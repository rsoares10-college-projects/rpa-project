#RPA Project

- Levantar estrutura
``` docker-compose up```

# MYSQL | Estrutura Tabelas

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


 TABELA: TOTAL_REQUESTS
 - DATA_REFERENCIA 
 - QUANTIDADE
 - ENDPOINT


# SCRIPT | PYTHON

Objetivo: Dentro do folder ``` ./app ``` temos um arquivo final.zip, nele contem todos os registros de covid disponíveis neste link do gitHub:
https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time_changesOnly.csv.gz


Com este ``` scrypt.py ``` vamos descompactar todos os dados no arquivo final.zip, organizar os dados e inserir nas duas tabelas citadas acima


# API FLASK

- ``` localhost:5000/total ```   -> acessa todos os registros do banco (soma por estados do dia) 
- ``` localhost:5000/total/estados ```   -> acessa todos os registros do banco por estado
- ``` localhost:5000/requests ```   -> retorna quantidade de acessos dos enpoints daquele dia em questão

