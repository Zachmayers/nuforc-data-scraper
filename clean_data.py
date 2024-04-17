import pandas as pd
import sys
import os

BAD_CHARACTERS = ['(', ')', '{','}', '/', ',','.', '+', 'unknown']

def has_bad_character(city):
    if type(city) is not str:
        return True
    
    for ch in BAD_CHARACTERS:
        if ch in city:
            return True

    spl = city.split(' ')
    if len(city.split(' ')) > 3:
        return True

    return False

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please provide CSV file path')
        sys.exit()

    file_path = sys.argv[1]
    try:
        df = pd.read_csv(file_path)
        df = df.replace(r'\n',' ', regex=True) 
        cols_to_remove = ['Link', 'Media']
        df.drop(cols_to_remove, axis=1, inplace=True)
        print(f'Removing the following unneeded columns: {cols_to_remove}')

        prev_len = len(df)
        cities = df.City.unique()
        print(f'Found {len(cities)} unique cities in data.')

        badly_formatted_cities = []
        for i, city in enumerate(cities):
            try:
                if has_bad_character(city):
                    badly_formatted_cities.append(city)
            except Exception as e:
                print(e)

        print(f'Found {len(badly_formatted_cities)} city names that were formatted poorly.')
        df = df[~df['City'].isin(badly_formatted_cities)]
        print(f'Removed {prev_len - len(df)} rows from DataFrame due to bad formatting.')
        
        output_path = f'{os.path.dirname(file_path)}/CLEANED_{os.path.basename(file_path)}'

        df.to_csv(output_path, index=False)
        print(f"Cleaned data and outputted to {output_path}")
    except Exception as e:
        print(e)