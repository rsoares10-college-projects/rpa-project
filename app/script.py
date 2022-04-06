from dataclasses import fields
import objects.DatabaseUtils as db
import pandas as pd
from zipfile import ZipFile
from flask import Flask
from flask import request
import requests
from datetime import datetime
import json
import smtplib, ssl


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


app = Flask(__name__)

@app.route("/total/estados")
def totalPorEstado():
    data_engine = db.database()
    data_referencia = datetime.today().strftime('%Y-%m-%d')

    values_request = {
        "data_referencia": data_referencia,
        "endpoint": "total/estados"
    }
    
    data_engine.add_requests(values=values_request)
    total = data_engine.get_total_estados()

    return json.dumps(total, indent=4, sort_keys=True, default=str)


@app.route("/total")
def total():
    data_engine = db.database()
    data_referencia = datetime.today().strftime('%Y-%m-%d')

    values_request = {
        "data_referencia": data_referencia,
        "endpoint": "total"
    }
    
    data_engine.add_requests(values=values_request)
    total = data_engine.get_total()
    return json.dumps(total, indent=4, sort_keys=True, default=str)



@app.route("/requests")
def requests():
    data_engine = db.database()
    data_referencia = datetime.today().strftime('%Y-%m-%d')

    values_request = {
        "data_referencia": data_referencia
    }
    
    todos_requests = data_engine.get_requests(values=values_request)

    #port = 465  # For SSL
    #smtp_server = "smtp.gmail.com"
    #sender_email = "sbardelatt@gmail.com"  
    #receiver_email = "sbardelatt@gmail.com"  
    #password = "****"

    #tipos_de_ingresso = []

    #message = "Subject: Report diário requests\n\n"
    #for tipo in tipos_de_ingresso:
    #    for k, v in tipo.items():
    #        message += f"{k}: {v}\n"
    #        message += "\n"

    #context = ssl.create_default_context()
    #with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #    server.login(sender_email, password)
    #    server.sendmail(sender_email, receiver_email, message.encode('utf-8'))

    return json.dumps(todos_requests)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')