#RPA Project

- Levantar estrutura
``` docker-compose up```

MYSQL | Estrutura Tabelas

TABELA: HISTORICO_COVID_POR_ESTADOS
 - DATA_REFERENCIA 
 - STATE
 - DEATHS 
 - TOTAL_CASES 
 - NEW_DEATHS 
 - NEW_CASES 


 TABELA: HISTORICO_COVID_TOTAIS
 - DATA_REFERENCIA 
 - DEATHS 
 - TOTAL_CASES 
 - NEW_DEATHS 
 - NEW_CASES 



SCRIPT PYTHON

Objetivo: Dentro do folder ``` ./app ``` temos um arquivo final.zip, nele contem todos os registros de covid disponíveis neste link do gitHub:
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/03-31-2021.csv


Com este ``` scrypt.py ``` vamos descompactar todos os dados no arquivo final.zip, organizar os dados e inserir nas duas tabelas citadas acima

