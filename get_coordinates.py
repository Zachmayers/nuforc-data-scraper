import requests
import pandas as pd
import json
import os
import sys

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide CSV file path')
        sys.exit()

    file_path = sys.argv[1]
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address=Akron&components=administrative_area:pa&key={API_KEY}"

        df = pd.read_csv(file_path)
        cities = df.City.unique()

        data = []
        for city in cities:
            try:
                print(f'looking up {city}')
                res = requests.get(url)   
                parsed_res = json.loads(res.content)
                data.append((city ,parsed_res['results'][0]['geometry']['location']))

            except Exception as e:
                print(e)

        lats = {}
        longs = {}
        for coord in data:
            city = coord[0]
            lat = coord[1]["lat"]
            lng = coord[1]["lng"]
            lats[city] = lat
            longs[city] = lng
        
        df['lat'] = df['City'].map(lats)
        df['lng'] = df['City'].map(longs)
        output_path = f'{os.path.dirname(file_path)}/FULL_{os.path.basename(file_path)}'
        df.to_csv(output_path, index=False)
        print(f'Outputted data with Coordinates included to {output_path}')

    except Exception as e:
        print(e)
