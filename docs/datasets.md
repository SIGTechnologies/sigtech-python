# Datasets

Datasets provide a method to get data from your local environment/machine
into the SigTech research environment.

This guide provides instructions on how to use the SigTech 
Datasets command-line interface (CLI) within your terminal. 


With these commands, you can list datasets, upload files to 
a dataset, and delete files from a dataset.


## Getting Started
Before you begin, ensure you have Python installed on your machine
and that you have installed the SigTech Python SDK. 

You will also need to create a Personal Access Token within the platform
and set the environment variable `SIGTECH_PLATFORM_TOKEN`
to the value of this token.

For Windows:
    
    setx SIGTECH_PLATFORM_TOKEN <YOUR_ACCESS_TOKEN>

For macOS and Linux:

    export SIGTECH_PLATFORM_TOKEN=<YOUR_ACCESS_TOKEN>


To create a Personal Access Token visit https://platform.sigtech.com/settings.


## Python

```python
from sigtech.api.datasets import DatasetsApi
api = DatasetsApi()

# List all datasets
api.datasets.df()

# Create a new dataset via CSV upload
api.datasets.upload("path/to/local/file.csv", "my_dataset")

# List all files within the dataset
api.datasets["my_dataset"].files.df()
```




## CLI 

### Listing datasets & files


List all datasets: 

    python -m sigtech.api.datasets ls


List all files within a dataset: 

    python -m sigtech.api.datasets ls <dataset_id>


List files that match a pattern within a dataset: 

    python -m sigtech.api.datasets ls '<dataset_id>/some-file-pattern*'



### Uploading data

Upload a local CSV file to a dataset 

    python -m sigtech.api.datasets cp path/to/data.csv <dataset_id>



### Deleting files from a dataset

Delete a single file from a dataset: 

    python -m sigtech.api.datasets rm <dataset_id>/<file_id>

Delete all files matching a pattern from a dataset: 

    python -m sigtech.api.datasets rm <dataset_id>/some-file-pattern*
