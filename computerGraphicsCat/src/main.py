import tarfile
import os

# Specify the path to your tar.gz file
dataset_path = "C:/Users/Michael Owen/Downloads/amazon-massive-dataset-1.1_CAT1.tar.gz"

# Specify the directory where you want to extract the files
extraction_directory = "C:/Users/Michael Owen/PycharmProjects/computerGraphicsCat/data/extracted_dataset"

# Create the extraction directory if it doesn't exist
os.makedirs(extraction_directory, exist_ok=True)

# Extract the tar.gz file
with tarfile.open(dataset_path, 'r:gz') as tar:
    tar.extractall(path=extraction_directory)
