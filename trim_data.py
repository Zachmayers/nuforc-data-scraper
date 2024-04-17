import sys
import os
import pandas as pd

YEARS_TO_INCLUDE = ['2019', '2020', '2021', '2022', '2023', '2024']

def good_year(year):
    return year.split(' ')[0].split('/')[2] in YEARS_TO_INCLUDE

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please provide CSV file path')
        sys.exit()

    file_path = sys.argv[1]

    try:
        df = pd.read_csv(file_path)
        bad_indexes = []
        for i in df.iterrows():
            year = i[1]['Occurred']
            if type(year) is not str:
                bad_indexes.append(i[0])
                continue

            if not good_year(year):
                bad_indexes.append(i[0])

        print(f'Removing {len(bad_indexes)} rows from DataFrame')
        df.drop(index=bad_indexes, inplace=True)
        output_path = f'{os.path.dirname(file_path)}/{YEARS_TO_INCLUDE[0]}_to_{YEARS_TO_INCLUDE[-1]}-ONLY_{os.path.basename(file_path)}'
        df.to_csv(output_path, index=False)
        print(f'Trimmed data and outputted to {output_path}')

    except Exception as e:
        print(e)