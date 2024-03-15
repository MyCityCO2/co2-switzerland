import pandas as pd
import os

filename = 'BFS_Geodata'
datafolder = 'data'
path = os.path.join(datafolder, filename+'.xlsx')
zipcode_path = os.path.join(datafolder, "Zip_codes.csv")
pop_path = os.path.join(datafolder, "population.xlsx")

gde_df = pd.read_excel(path, sheet_name="GDE")[['GDEKT', 'GDENR', 'GDENAME']]
kt_df = pd.read_excel(path, sheet_name="KT")[['GDEKT', 'KTNR']]
pop_df = pd.read_excel(pop_path)
zip_df = pd.read_csv(zipcode_path, sep = ';')[['Ortschaftsname', 'PLZ', 'BFS-Nr']]

pop_df['GDENR'] = pop_df['id_city'].apply(lambda x: str(x).zfill(4))
pop_df.drop(columns=['id_city', 'city'], inplace=True)

zip_df['GDENR'] = zip_df['BFS-Nr'].apply(lambda x: str(x).zfill(4))
zip_df.drop(columns=['BFS-Nr'], inplace=True)
zip_df.rename(inplace=True, columns={'Ortschaftsname' : 'Ortschaftsname'.upper()})

ktname_to_ktnumber = kt_df.set_index('GDEKT').squeeze().to_dict()

gde_df['KTNR'] = gde_df['GDEKT'].map(ktname_to_ktnumber)
gde_df['GDENR'] = gde_df['GDENR'].apply(lambda x: str(x).zfill(4))
gde_df['KTNR'] = gde_df['KTNR'].apply(lambda x: str(x).zfill(2))
gde_df['UID'] = gde_df['KTNR'] + gde_df['GDENR']

result_df = pd.merge(gde_df,zip_df,on='GDENR',how='outer').dropna()
result_df['PLZ'] = result_df['PLZ'].astype(int)

result_df.to_csv(os.path.join(datafolder, filename+'_concat.csv' ), index=False)