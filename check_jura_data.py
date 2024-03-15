import pandas as pd
import os
import warnings
import numpy as np

year = 2022
filename = '4.2.-Compte-de-resultats-par-commune.'+str(year)
index_header = 2

test_filename = filename+'_clean.csv'
truth_filename = filename+'.xlsx'

datafolder = 'data'
test_path = os.path.join(datafolder, test_filename)
truth_path = os.path.join(datafolder, truth_filename)

test_df = pd.read_csv(test_path)
truth_df = pd.read_excel(truth_path, header=index_header, sheet_name="4.1 Comptes "+str(year)+" natures")

# keep only sum over account aka categories stored in column of index 1
mask = truth_df.iloc[:,1].isnull()
truth_df= truth_df[~mask].dropna(axis=1).drop(columns = 'Unnamed: 3').rename(columns = {'Unnamed: 1' : 'category'})
truth_df['category'] = truth_df['category'].astype(int)
truth_df.set_index('category', inplace=True)

# clean test df to keep only sums pro categories
test_df['category'] = test_df['account'].astype(str).str[:2].astype(int)
test_df = test_df.groupby(['category', 'uid_city']).agg({'result' : 'sum'}).unstack()
test_df.columns = test_df.columns.droplevel()

categories = list(test_df.index)
cities_uid = list(test_df.columns)
bol = False

for cat in categories : 
    for uid in cities_uid : 
        test_value = np.round(test_df.loc[cat, uid], 3)
        truth_value = np.round(truth_df.loc[cat, uid], 3)

        if test_value != truth_value : 
            warnings.warn("Uid "+str(uid) + " of value "+str(test_value)+" does not correspond to the truth value of "+str(truth_value))