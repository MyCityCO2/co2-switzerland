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
path = os.path.join(datafolder, filename+'.'+filetype)

df = pd.read_excel(path, header=index_header, sheet_name="4.1 Comptes "+str(year)+" natures").dropna(axis = 0, how = 'all').dropna(axis = 1, how = 'all') # clean df from empty lines/columns

uid_to_cities_map = { k: v  for k,v in df.iloc[0].to_dict().items() if isinstance(k, int)} # keep city name and corresponding uid
df.drop(index = 0, inplace = True) # drop city name as they are saved above. TODO: save it as json ?

col_uid_label = list(df.columns)[index_uid_label] # retrieve the column uid-for-labels from defined index above
mask = df[col_uid_label].isna() # use it as mask as everything else is unnecessary lines
df = df[~mask].dropna(axis=1, how='any')

df.index = df[col_uid_label] #set label uid as index
df = df.rename_axis('uid', axis='index')

uid_to_label_map = { k: v  for k,v in df.iloc[0].to_dict().items() if isinstance(k, int)} # keep label name and corresponding uid
df =df.drop(columns= [c for c in df.columns if not isinstance(c, int)]) # drop every other columns as they unknown

df = df.loc[[uid for uid in df.index if len(str(uid)) == 3]] # keep only valid uid for labels

# pivot data and add other informations and save it
cleaned = df.stack().reset_index()
cleaned.columns = ['account', 'uid_city', 'result']
cleaned['city'] = cleaned['uid_city'].map(uid_to_cities_map)
cleaned['currency'] = 'CHF'
cleaned['chart_of_account'] = 'MCH2'
cleaned['country_iso'] = 'CH'
cleaned['date'] = datetime(year, 12, 31).strftime("%d.%m.%Y")
cleaned['identifier'] = 'to_be_defined'

cleaned.to_csv(os.path.join(datafolder, filename+'_clean.csv'), index=False)