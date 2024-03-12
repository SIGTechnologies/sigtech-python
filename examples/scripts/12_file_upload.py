import logging
import os

from sigtech.api.datasets import DatasetsApi

logging.basicConfig(level=logging.DEBUG)

api = DatasetsApi()

# Path to the file to upload - replace with your own path
path = os.path.join(
    "<SIGTECH_ROOT_DIR>", "examples", "scripts", "data", "sample_data.csv"
)

# Upload a file to a dataset - replace with your own dataset_id
api.datasets.upload(path, "test_dataset_sdk")


# Load the dataset in the Jupyter platform via:
# from sigtech.framework.infra.platform import data_tools
# data_tools.get_dataset("test_dataset_sdk")
