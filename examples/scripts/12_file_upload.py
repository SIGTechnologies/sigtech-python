import logging

from sigtech.api.datasets import DatasetsApi

logging.basicConfig(level=logging.DEBUG)

api = DatasetsApi()

# Create a sample data file to upload
with open("sample_data.csv", "w") as f:
    f.write("ticker,date,price\nEX1,2018-01-01,100.123\nEX1,2018-01-01,100.123\n")


# Upload a file to a dataset - replace with your own dataset_id
api.datasets.upload("sample_data.csv", "test_dataset_sdk")


# Load the dataset in the Jupyter platform via:
# from sigtech.framework.infra.platform import data_tools
# data_tools.get_dataset("test_dataset_sdk")
