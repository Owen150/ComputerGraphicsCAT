import tarfile
import os

# Specify the path to your tar.gz file
dataset_path = "data/your_dataset.tar.gz"

# Specify the directory where you want to extract the files
extraction_directory = "data/extracted_dataset"

# Create the extraction directory if it doesn't exist
os.makedirs(extraction_directory, exist_ok=True)

# Extract the tar.gz file
with tarfile.open(dataset_path, 'r:gz') as tar:
    tar.extractall(path=extraction_directory)
