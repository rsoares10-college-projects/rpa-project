from dataclasses import fields
import objects.DatabaseUtils as db
import pandas as pd
from zipfile import ZipFile


z = ZipFile('final.zip', 'r')
z.extractall()
z.close()

df = pd.read_csv('dados.csv')

# tratamento de colunas
df.rename(columns={"newDeaths": "new_deaths", "newCases": "new_cases", "totalCases" : "total_cases"}, inplace=True)
df['data_referencia'] = pd.to_datetime(df['date'], format='%Y-%m-%d')


# agrupando e ordenando 
df_final = df.groupby(['data_referencia','state']).sum()[["deaths", "total_cases", "new_deaths", "new_cases"]]
df_final = df_final.reset_index()
df_final = df_final.sort_values(by='data_referencia')

#df_estados = df_final[df_final["state"].str.contains("TOTAL")==False]

data_engine = db.database()
tabela_ja_existente = 0

try:
    print('Criando tabelas...')
    data_engine.execute_from_query(sql_file='database.sql')
except:
    tabela_ja_existente = 1
    print("Tabela já existente")


def inserir_dados_mysql(df, data_engine):
    dados = df.shape[0]
    for i in range(0, dados):
        values = df.iloc[i].to_dict()
        data_engine.ingest(values=values)


if tabela_ja_existente == 0:
    print('Inserindo dados MYSQL...')
    data_engine = db.database()
    inserir_dados_mysql(df_final, data_engine)


