import tarfile
import json
import pandas as pd
from openpyxl import Workbook

# File path to the .tar.gz archive
tar_path = 'data'

if not tarfile.is_tarfile(tar_path):
    print(f"{tar_path} is not a valid .tar.gz file.")
else:
    with tarfile.open(tar_path, 'r:gz') as tar:
        jsonl_files = [member for member in tar.getmembers() if member.name.endswith('.jsonl')]

        if jsonl_files:
            amazon_data = []
            for jsonl_file in jsonl_files:
                json_data = tar.extractfile(jsonl_file).read().decode('utf-8')
                amazon_data += [json.loads(line) for line in json_data.split('\n') if line.strip()]

            if amazon_data:
                df = pd.DataFrame(amazon_data)

                # Create an Excel (.xlsx) file for all languages
                with pd.ExcelWriter('en-xx.xlsx', engine='xlsxwriter') as writer:
                    for locale in df['locale'].unique():
                        locale_data = df[df['locale'] == locale][['id', 'utt', 'annot_utt']]
                        locale_data.to_excel(writer, sheet_name=locale, index=False)

                # Filter data for English (en), Swahili (sw), and German (de)
                target_locales = ['en', 'sw', 'de']
                for locale in target_locales:
                    for partition in ['test', 'train', 'dev']:
                        locale_partition_data = df[(df['locale'] == locale) & (df['partition'] == partition)]
                        filename = f'{locale}_{partition}.json'
                        locale_partition_data.to_json(filename, orient='records', lines=True, force_ascii=False, indent=4)


                # Create a single JSON file with translations from en to xx for the train set
                train_data_en_to_xx = df[(df['locale'] == 'en') & (df['partition'] == 'train')]
                train_data_xx = df[(df['locale'].isin(target_locales)) & (df['partition'] == 'train')]

                def get_translation(locale):
                    xx_data = train_data_xx[train_data_xx['locale'] == locale]
                    return xx_data[['id', 'utt']].rename(columns={'utt': locale})

                for xx_locale in target_locales:
                    train_data_en_to_xx = train_data_en_to_xx.merge(get_translation(xx_locale), on='id', how='left')

                train_data_en_to_xx.to_json('en_to_xx_train.json', orient='records', lines=True, force_ascii=False, indent=4)

            else:
                print("No data found in the JSONL files.")
        else:
            print("No JSONL files found in the .tar.gz archive.")