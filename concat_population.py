import pandas as pd
import os

datafolder = 'data'
filename = 'BFS_Geodata'
pop_path = os.path.join(datafolder, "population.xlsx")
path = os.path.join(datafolder, filename+'.xlsx')

gde_df = pd.read_excel(path, sheet_name="GDE")[['GDEKT', 'GDENR', 'GDENAME']]
kt_df = pd.read_excel(path, sheet_name="KT")[['GDEKT', 'KTNR']]
pop_df = pd.read_excel(pop_path)

pop_df['GDENR'] = pop_df['id_city'].apply(lambda x: str(x).zfill(4))
pop_df.drop(columns=['id_city', 'city'], inplace=True)

ktname_to_ktnumber = kt_df.set_index('GDEKT').squeeze().to_dict()

gde_df['KTNR'] = gde_df['GDEKT'].map(ktname_to_ktnumber)
gde_df['GDENR'] = gde_df['GDENR'].apply(lambda x: str(x).zfill(4))
gde_df['KTNR'] = gde_df['KTNR'].apply(lambda x: str(x).zfill(2))
gde_df['UID'] = gde_df['KTNR'] + gde_df['GDENR']

result_df = pd.merge(gde_df, pop_df, on='GDENR', how = 'right')

result_df.to_csv(os.path.join(datafolder, 'population_output.csv' ), index=False)