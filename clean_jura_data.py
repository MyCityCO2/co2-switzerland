import pandas as pd
import os
from datetime import datetime

# set the index of the wanted columns (for example city as uid and label as uid here) - rememeber they start from 0
index_header = 2
index_uid_label = 2
year = 2022

filetype = 'xlsx'
filename = '4.2.-Compte-de-resultats-par-commune.'+str(year)
datafolder = 'data'
geo_filename = 'BFS_Geodata_concat.csv'
path = os.path.join(datafolder, filename+'.'+filetype)

df = pd.read_excel(path, header=index_header, sheet_name="4.1 Comptes "+str(year)+" natures").dropna(axis = 0, how = 'all').dropna(axis = 1, how = 'all') # clean df from empty lines/columns
geo_df = pd.read_csv(os.path.join(datafolder, geo_filename))

city_to_uid = geo_df[['GDENAME', 'UID']].set_index('GDENAME').squeeze().to_dict()

cities_to_pop = { v: k  for k,v in df.iloc[0].to_dict().items() if isinstance(k, int)} # keep city name and corresponding population
df.columns = df.iloc[0]
df.drop(index = 0, inplace = True) # drop city name as they are used as column name

mask = df.iloc[:,index_uid_label].isna() # use it as mask as everything else is unnecessary lines
df = df[~mask].dropna(axis=1, how='any')

df.index = df.iloc[:,0] #set label uid as index
df = df.rename_axis('uid', axis='index')

df =df.drop(columns= [c for c in df.columns if pd.isnull(c) or c not in list(city_to_uid.keys())]) # drop every other columns as they unknown
df = df.loc[[uid for uid in df.index if len(str(uid)) == 3]] # keep only valid uid for labels
df.columns.name = 'city_name'

# pivot data and add other informations and save it
cleaned = df.stack().reset_index()
cleaned.columns = ['account', 'city_name', 'result']
cleaned['identifier'] = cleaned['city_name'].map(city_to_uid)
cleaned['population'] = cleaned['city_name'].map(cities_to_pop)
cleaned['currency'] = 'CHF'
cleaned['chart_of_account'] = 'MCH2'
cleaned['country_iso'] = 'CH'
cleaned['date'] = datetime(year, 12, 31).strftime("%d.%m.%Y")

cleaned.to_csv(os.path.join(datafolder, filename+'_clean.csv'), index=False)