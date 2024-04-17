import json
import pandas as pd

with open('coords.txt', 'r') as f:
    d = f.read()

coords = json.loads(d)

df = pd.read_csv('2020_to_2024_only.csv')

lats = {}
longs = {}

for i in coords:
    lats[i] = coords[i]['lat']
    longs[i] = coords[i]['lng']

df['lat'] = df['City'].map(lats)
df['lng'] = df['City'].map(longs)

df.to_csv('FINALLY.csv', index=False)