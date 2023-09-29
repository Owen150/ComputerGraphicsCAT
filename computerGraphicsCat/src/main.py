import tarfile
import os
import pandas as pd

# Specify the path to your tar.gz file
dataset_path = "C:/Users/Michael Owen/Downloads/amazon-massive-dataset-1.1_CAT1.tar.gz"

# Specify the directory where you want to extract the files
extraction_directory = "C:/Users/Michael Owen/PycharmProjects/computerGraphicsCat/data/extracted_dataset"

# Create the extraction directory if it doesn't exist
os.makedirs(extraction_directory, exist_ok=True)

# Extract the tar.gz file
with tarfile.open(dataset_path, 'r:gz') as tar:
    tar.extractall(path=extraction_directory)


# Load the English dataset (assuming it's called 'en.xlsx')
english_dataset_path = os.path.join(extraction_directory, 'en.xlsx')
english_df = pd.read_excel(english_dataset_path)

# Create a dictionary to store dataframes for each language
language_dataframes = {}

# Loop through files in the extraction directory
for filename in os.listdir(extraction_directory):
    if filename.endswith(".xlsx") and filename != 'en.xlsx':
        language_code = os.path.splitext(filename)[0]
        language_df = pd.read_excel(os.path.join(extraction_directory, filename))

        # Merge English data with the current language's data based on ID
        merged_df = pd.merge(english_df[['id', 'utt', 'annot_utt']],
                             language_df[['id', 'utt', 'annot_utt']],
                             on='id')

        # Save the merged dataframe to en-xx.xlsx
        output_path = os.path.join("output", f"en-{language_code}.xlsx")
        merged_df.to_excel(output_path, index=False)
