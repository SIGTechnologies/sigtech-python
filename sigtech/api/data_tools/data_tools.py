import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from io import BytesIO
import requests
import pandas as pd
import logging

logger = logging.getLogger("datatools")


class DataTools:
    """
    Collection of utilities for data injection and extraction.

    Custom Data interface:

        * ``create_dataset``: Create a new structured or unstructured dataset.
        * ``list_datasets``: Return a list of available datasets and their
        metadata.
        * ``list_dataset_files``: Given a dataset identifier, return a list of
        the available files and their metadata.
        * ``get_dataset_info``: Given a dataset identifier, return a dict
        containing all metadata available for the dataset.
        * ``get_file_info``: Given a dataset identifier and a file identifier,
        return a dict containing all metadata available for the file.
        * ``upload_data``: Upload data to the given dataset. If a string is
        provided, upload a file with that name and use the file extension for
        the format type. If a DataFrame is provided, upload it using the format
        from the file's extension.
        * ``get_data``: Given a dataset identifier, retrieve the available data.
        If a file identifier is provided, retrieve only the specified file.
        If a file is not provided and the dataset is structured, retrieve all
        available data.
        * ``delete_dataset``: Delete a dataset.
        * ``delete_file``: Delete a file or multiple files from a dataset.


    Strategy Deployment interface:

        * ``list_deployments``: Return a list of available deployments and
        their metadata.
        * ``list_deployment_executions``: Given a deployment identifier, return
        a DataFrame with all available executions for the deployment.
        * ``list_deployment_outputs``: Given a deployment identifier and an
        execution identifier, return a Dataframe containing all available
        strategy outputs.
        * ``get_deployment_output``: Given a deployment identifier, an execution
        identifier and an output filename, return a Dataframe containing the
        output data.  If execution_id is not provided, then retrieve the output
        from the latest execution.

    """
    _RECORDS_PER_PAGE = 100  # Max numbers of records per page returned
    _MAX_ITERATIONS = 10
    _client_data_url = os.getenv('CLIENT_DATA_URL',
                                 'https://enterprise-api.sigtech.com')
    _sd_url = os.getenv('CLIENT_DATA_URL', 'https://enterprise-api.sigtech.com')
    _ingestion_url = f'{_client_data_url}/ingestion/v2/datasets'
    _extraction_url = f'{_sd_url}/extraction/v2/deployments'
    _token = os.getenv('SIGTECH_PLATFORM_TOKEN')
    _headers = {'Authorization': f'Bearer {_token}'}
    _session = requests.Session()

    # Configure retry logic
    retries = Retry(
        total=3,  # Number of retries
        # {backoff_factor} * (2 ** ({number_retries} - 1)), so 0.3s, 0.6s, 1.2s
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST", "DELETE"]
    )
    _session.mount('https://', HTTPAdapter(max_retries=retries))
    _session.headers.update(_headers)

    @classmethod
    def _send(cls, method: str, url: str, **kwargs):
        if method not in ['GET', 'POST', 'DELETE']:
            raise ValueError(f"Unsupported HTTP method: {method}. "
                             f"Allowed methods are 'GET', 'POST', and 'DELETE'.")

        # Use the shared session with retry
        if method == 'GET':
            resp = cls._session.get(url, **kwargs)
        elif method == 'POST':
            resp = cls._session.post(url, **kwargs)
        elif method == 'DELETE':
            resp = cls._session.delete(url, **kwargs)

        # Handle the response
        details = resp.json() if resp.content or resp.text else None
        if not str(resp.status_code).startswith('2'):
            msg = '' if not details else details.get('message', '')
            msg_fmt = f': {msg}' if msg else ''
            raise RuntimeError(f'Client data service request failed with code '
                               f'{resp.status_code}{msg_fmt}')

        return details

    @classmethod
    def _paginate(cls, url: str):
        data = []
        for page in range(1, cls._MAX_ITERATIONS + 1):
            resp_json = cls._send('GET', url,
                                  params={'limit': str(cls._RECORDS_PER_PAGE),
                                          'page': str(page)})
            data.extend(resp_json['data'])
            if len(data) >= resp_json['count']:
                break
        return pd.DataFrame(data).set_index(['id']).rename_axis(None) \
            if data else None

    @classmethod
    def _df_from_pre_signed_url(cls, url, extension, date_cols):
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f'Client data request failed with code '
                               f'{response.status_code}')

        binary_data = BytesIO(response.content)
        if extension == 'csv':
            df = pd.read_csv(binary_data)
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], utc=True)
        elif extension == 'parquet':
            df = pd.read_parquet(binary_data)
        else:
            raise ValueError(f'Unrecognized file type: {extension}')
        return df

    @classmethod
    def list_datasets(cls) -> pd.DataFrame:
        """ Return a list of available datasets and their metadata. """
        df = cls._paginate(cls._ingestion_url)
        df = df.drop('ownerId', axis=1)
        data = {'schema': [], 'owner': [], 'isStructured': []}
        for dataset_id in df.index:
            dct = cls.get_dataset_info(dataset_id)
            data['isStructured'].append(dct['isStructured'])
            data['schema'].append(dct['schema'])
            data['owner'].append(dct['owner']['emailAddress'])
        return pd.DataFrame({**df.to_dict(orient='list'), **data},
                            index=df.index)

    @classmethod
    def create_dataset(cls, name: str, schema: dict = None,
                       permission_level: str = 'write'):
        """
        Create a new structured or unstructured dataset.

        :param name: Name of the dataset.
        :param schema: Schema of the dataset. If not specified, the dataset
        will be considered unstructured.
        :param permission_level: Permission level of the dataset.
        Available options are 'read' and 'write'.
        """

        if type(name) is not str or not name:
            raise ValueError('Name must be a non-empty string')
        if permission_level not in ['read', 'write']:
            raise ValueError("Permission level must be 'read' or 'write'")
        if schema is not None and type(schema) is not dict:
            raise ValueError('Schema must be of type dict')
        if schema and not all([type(i) is str for i in schema.values()]):
            raise ValueError('Schema dict must contain all values of type string')
        params = {
            'name': name,
            'permissionType': 'organisation',
            'permissionLevel': permission_level,
            'isStructured': True if schema else False,
            'schema': schema,
        }
        cls._send('POST', cls._ingestion_url, json=params)

    @classmethod
    def list_dataset_files(cls, dataset_id: str) -> pd.DataFrame:
        """
        Given a dataset identifier, return a list of the available files
        and their metadata.

        :param dataset_id: Dataset identifier.
        :return: pandas DataFrame.
        """
        df = cls._paginate(f'{cls._ingestion_url}/{dataset_id}/files')
        if df is None or df.empty:
            return pd.DataFrame()
        data = {'size': [], 'createdAt': [], 'owner': []}
        for file_id in df.index:
            dct = cls.get_file_info(dataset_id, file_id)
            data['size'].append(dct['size'])
            data['createdAt'].append(dct['createdAt'])
            data['owner'].append(dct['createdBy']['emailAddress'])
        return pd.DataFrame({**df.to_dict(orient='list'), **data}, index=df.index)

    @classmethod
    def get_dataset_info(cls, dataset_id: str) -> dict:
        """
        Given a dataset identifier, return a dict containing all metadata
        available for the dataset.

        :param dataset_id: Dataset identifier.
        :return: dict.
        """
        return cls._send('GET', f'{cls._ingestion_url}/{dataset_id}')

    @classmethod
    def get_file_info(cls, dataset_id: str, file_id: str) -> dict:
        """
        Given a dataset identifier and a file identifier, return a dict
        containing all metadata available for the file.

        :param dataset_id: Dataset identifier.
        :param file_id: File identifier.
        :return: dict.
        """
        return cls._send('GET',
                         f'{cls._ingestion_url}/{dataset_id}/files/{file_id}')

    @classmethod
    def upload_data(cls, dataset_id: str, name: str, df: pd.DataFrame = None):
        """
        Upload data to the given dataset. If a string is provided, upload a
        file with that name and use the file extension for the format type.
        If a DataFrame is provided, upload it using the format from the file's
        extension.

        :param dataset_id: Dataset identifier.
        :param name: Name for the uploaded file (optional if ``data`` is a filename).
        :param df: DataFrame to be uploaded (optional).
        """
        extension = name.split('.')[-1].lower()
        if extension not in ['csv', 'parquet']:
            raise ValueError(f'Unrecognised extension for {name}. '
                             f'Available types are "parquet" and "csv"')
        if df is None:
            if extension == 'parquet':
                df = pd.read_parquet(name, engine='pyarrow')
            elif extension == 'csv':
                df = pd.read_csv(name)
        buffer = BytesIO()
        if extension == 'parquet':
            ext = 'application/octet-stream'
            df.to_parquet(buffer, engine='pyarrow')
        elif extension == 'csv':
            ext = 'text/csv'
            df.to_csv(buffer, index=False)
        buffer.seek(0)
        files = {
            'file': (name, buffer.read() if extension == 'csv' else buffer, ext),
            'name': (None, name),
        }
        cls._send('POST', cls._ingestion_url + f'/{dataset_id}/files',
                  files=files)

    @classmethod
    def get_data(cls, dataset_id: str, file_id: str = None,
                 date_cols: list = None) -> pd.DataFrame:
        """
        Given a dataset identifier, retrieve the available data.
        If a file identifier is provided, retrieve only the specified file.
        If a file is not provided and the dataset is structured, retrieve all
        available data.

        :param dataset_id: Dataset identifier.
        :param file_id: File identifier (optional).
        :param date_cols: List of column names that will be parsed as `date`,
        `time`, `datetime` or `Timestamp`. (optional, it only applies to CSV files).
        :return: pandas DataFrame.
        """
        dataset_dct = cls.get_dataset_info(dataset_id)
        is_structured = dataset_dct.get('isStructured', None)
        if is_structured is None or type(is_structured) is not bool:
            raise ValueError(f'Client data request for dataset {dataset_id} '
                             f'failed: structure {is_structured}')
        if not is_structured and file_id is None:
            raise ValueError(f'Dataset {dataset_id} is not structured, please '
                             f'specify a file identifier')
        params = {} if file_id is None else {'fileIds': f'{file_id}'}
        resp = cls._send('GET',
                         f'{cls._ingestion_url}/{dataset_id}/files/contents',
                         params=params)
        if not resp or 'files' not in resp or not resp['files']:
            raise RuntimeError(f'Client data request for dataset {dataset_id} '
                               f'failed: no files available')
        data = []
        for file in resp['files']:
            _url, extension = file['url'], file['fileExtension']
            data.append(cls._df_from_pre_signed_url(_url, extension.lower(),
                                                    date_cols if date_cols else []))
        if len(data) == 1:
            return data[0]
        # Attempt collating the files: check all files have same columns
        same_structure = all(df.columns.tolist() == data[0].columns.tolist()
                             for df in data)
        if not same_structure:
            structure_dct = {dct['name']: df.columns.tolist()
                             for dct, df in zip(resp['files'], data)}
            raise RuntimeError(f'File structure mismatch for dataset '
                               f'{dataset_id}: {structure_dct}')
        return pd.concat(data, axis=0)

    @classmethod
    def delete_dataset(cls, dataset_id: str):
        """
        Delete a dataset.

        :param dataset_id: Dataset identifier.
        """
        cls._send('DELETE', cls._ingestion_url + f'/{dataset_id}')

    @classmethod
    def delete_file(cls, dataset_id: str, file_id: str):
        """
        Delete a file or multiple files from a dataset.

        :param dataset_id: Dataset identifier.
        :param file_id: File identifier. If the special string ``'*'`` is used,
        then delete all files.
        """
        url = cls._ingestion_url + f'/{dataset_id}/files'
        if file_id != '*':
            url += f'/{file_id}'
        cls._send('DELETE', url)

    @classmethod
    def list_deployments(cls) -> pd.DataFrame:
        """ Return a list of available deployments and their metadata. """
        df = cls._paginate(cls._extraction_url)
        df = df.drop(['userId', 'subStatus', 'failureReason'], axis=1)
        return df

    @classmethod
    def _clean_data_resp(cls, deployment_id: str, ret: any,
                         idx_name: str) -> pd.DataFrame:
        if ret and 'data' in ret:
            df = pd.DataFrame(ret['data'])
            if 'id' in df.columns:
                df = df.set_index('id')
            df.index.name = idx_name
            return df
        raise RuntimeError(f'Metadata retrieval failed for deployment {deployment_id}')

    @classmethod
    def list_deployment_executions(cls, deployment_id: str) -> pd.DataFrame:
        """
        Given a deployment identifier, return a DataFrame with all available
        executions for the deployment.

        :param deployment_id: Deployment identifier.
        :return: pandas DataFrame.
        """
        ret = cls._send('GET',
                        f'{cls._extraction_url}/{deployment_id}/executions')
        return cls._clean_data_resp(deployment_id, ret, 'executionId')

    @classmethod
    def list_deployment_outputs(cls, deployment_id: str,
                                execution_id: str = None) -> pd.DataFrame:
        """
        Given a deployment identifier and an execution identifier, return a
        Dataframe containing all available strategy outputs.

        :param deployment_id: Deployment identifier.
        :param execution_id: Execution identifier. If not provided, then
        retrieve the latest execution.
        :return: pandas DataFrame.
        """
        base_url = f'{cls._extraction_url}/{deployment_id}/executions'
        url = f'{base_url}/{execution_id}/outputs' if execution_id is not None \
            else f'{base_url}/latest/outputs'
        ret = cls._send('GET', url)
        df = cls._clean_data_resp(deployment_id, ret, 'outputId')
        if 'name' in df.columns:
            # csv files not supported by the deployment API (yet)
            df = df[~df['name'].str.lower().str.endswith('.csv')]
            # log files not supported by the deployment API (yet)
            df = df[~df['name'].str.lower().str.endswith('.log')]
            # JSON format of source SD notebook
            df = df[df['name'].str.lower() != 'results.json']
        return df

    @classmethod
    def get_deployment_output(cls, deployment_id: str, output_name: str,
                              execution_id: str = None) -> pd.DataFrame:
        """
        Given a deployment identifier, an execution identifier and an output
        filename, return a Dataframe containing the output data.

        :param deployment_id: Deployment identifier.
        :param output_name: Output filename.
        :param execution_id: Execution identifier. If not provided, then
        retrieve the latest execution.
        :return: pandas DataFrame.
        """
        exec_url = f'/{execution_id}/outputs' if execution_id is not None \
            else '/latest/outputs'
        url = (f'{cls._extraction_url}/{deployment_id}/executions' + exec_url
               + f'/{output_name}')
        data = cls._send('GET', url)
        try:
            df = pd.DataFrame(data)
            if (df.index.dtype == 'object'
                    and not isinstance(df.index, pd.MultiIndex)):
                df.index = pd.to_datetime(df.index, format="%Y-%m-%dT%H:%M:%S.%fZ",
                                          errors='ignore', utc=True)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = pd.to_datetime(df[col], format='%Y-%m-%dT%H:%M:%S.%fZ',
                                             errors='ignore', utc=True)
            index_columns = [col for col in df.columns if 'index:' in col]
            if index_columns:
                df = df.set_index(index_columns)
                df.index.names = [i.replace('index:', '').lstrip()
                                  for i in df.index.names]
            return df
        except Exception as e:
            exec_id = execution_id if execution_id else '(latest)'
            raise RuntimeError(f'Output retrieval failed for deployment '
                               f'{deployment_id} and execution {exec_id}: {e}')
