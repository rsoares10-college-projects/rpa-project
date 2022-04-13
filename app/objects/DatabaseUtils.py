import mysql.connector
import os

from pandas import DataFrame

par_db = {
    "host": "172.17.0.1",
    "database": "covid",
    "user": "root",
    "password": "root",
}

class database:
    def __init__(self):
        self.dir = os.getcwd()
        self.cnx_mysql = mysql.connector.connect(
            host=par_db.get("host"),
            user=par_db.get("user"),
            database=par_db.get("database"),
            password=par_db.get("password"),
        )
        self.query_por_estado   = "insert into HISTORICO_COVID_POR_ESTADOS(DATA_REFERENCIA,STATE, NEW_DEATHS, NEW_CASES) values('{data_referencia}', '{state}',{new_deaths},{new_cases})"
        self.query_truncate_estados = "TRUNCATE TABLE HISTORICO_COVID_POR_ESTADOS;"
        self.query_requests     = "insert into TOTAL_REQUESTS(DATA_REFERENCIA, QUANTIDADE, ENDPOINT) values('{data_referencia}', {quantidade}, '{endpoint}')"
        self.query_get_requests_by_endpoint_date = "SELECT * FROM TOTAL_REQUESTS WHERE DATA_REFERENCIA = '{data_referencia}' AND ENDPOINT = '{endpoint}'"
        self.query_update_requests = "UPDATE TOTAL_REQUESTS SET QUANTIDADE = {quantidade} WHERE DATA_REFERENCIA = '{data_referencia}' AND ENDPOINT = '{endpoint}';"
        self.query_get_requests_date = "SELECT ENDPOINT, QUANTIDADE FROM  TOTAL_REQUESTS WHERE DATA_REFERENCIA = '{data_referencia}';"
        self.query_get_total_estados = "SELECT * FROM  HISTORICO_COVID_POR_ESTADOS;"

    #executa o arquivo database.sql para criar as tabelas iniciais
    def execute_from_query(self, sql_file):
        with open(self.dir + "/" + sql_file, "r") as reads:
            sqlScript = reads.read()
            cursor_cnxn_msql = self.cnx_mysql.cursor()
            cursor_cnxn_msql.execute(sqlScript)


    #insere os registros conforme a atualização 
    def ingest(self, values:dict):
        insert_query = self.query_por_estado.format(**values)
        cursor_cnxn_msql = self.cnx_mysql.cursor()
        cursor_cnxn_msql.execute(insert_query)
        self.cnx_mysql.commit()


    #caso haja o acesso em um endpoint em específico, é incrementado na tabela através da coluna "quantidade"
    def add_requests(self, values):
        get_query = self.query_get_requests_by_endpoint_date.format(**values)
        cursor_cnxn_msql = self.cnx_mysql.cursor(buffered=True)
        cursor_cnxn_msql.execute(get_query)

        valores_select = cursor_cnxn_msql.fetchall()
        if cursor_cnxn_msql.rowcount == 0: 
            values = {
                "data_referencia": values['data_referencia'],
                "quantidade": 1,
                "endpoint": values['endpoint']

            }
            insert_query = self.query_requests.format(**values)
            cursor_cnxn_msql = self.cnx_mysql.cursor(buffered=True)
            cursor_cnxn_msql.execute(insert_query)
            self.cnx_mysql.commit()

        else:
            values = {
                "data_referencia": values['data_referencia'],
                "quantidade": valores_select[0][1] + 1,
                "endpoint": values['endpoint']
            }

            insert_query = self.query_update_requests.format(**values)
            cursor_cnxn_msql = self.cnx_mysql.cursor(buffered=True)
            cursor_cnxn_msql.execute(insert_query)
            self.cnx_mysql.commit()


    # busca o total de acessos naquele endpoint pela data
    def get_requests(self, values:dict):
        insert_query = self.query_get_requests_date.format(**values)
        cursor_cnxn_msql = self.cnx_mysql.cursor(buffered=True, dictionary=True)
        cursor_cnxn_msql.execute(insert_query)
        valores_select = cursor_cnxn_msql.fetchall()
        self.cnx_mysql.commit()
        return valores_select



    # busca todos os registros de estados e registros totais da COVID na tabela HISTORICO_COVID_POR_ESTADOS
    def get_total_estados(self):
        insert_query = self.query_get_total_estados
        cursor_cnxn_msql = self.cnx_mysql.cursor(buffered=True, dictionary=True)
        cursor_cnxn_msql.execute(insert_query)
        valores_select = cursor_cnxn_msql.fetchall()
        self.cnx_mysql.commit()
        return valores_select


    # remove todos os registros da tabela HISTORICO_COVID_POR_ESTADOS permitindo assim, a insereção de novos registros sem gerar duplicidade
    def truncate_table_estados(self):
        query = self.query_truncate_estados
        cursor_cnxn_msql = self.cnx_mysql.cursor(buffered=True, dictionary=True)
        cursor_cnxn_msql.execute(query)
