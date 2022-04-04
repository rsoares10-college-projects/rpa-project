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
        self.query_por_estado = "insert into HISTORICO_COVID_POR_ESTADOS(DATA_REFERENCIA,STATE ,DEATHS,TOTAL_CASES, NEW_DEATHS, NEW_CASES) values('{data_referencia}', '{state}', {deaths}, {total_cases},{new_deaths},{new_cases})"
        self.query_totais     = "insert into HISTORICO_COVID_TOTAIS(DATA_REFERENCIA,DEATHS,TOTAL_CASES, NEW_DEATHS, NEW_CASES) values('{data_referencia}', {deaths}, {total_cases},{new_deaths},{new_cases})"

    def execute_from_query(self, sql_file):
        with open(self.dir + "/" + sql_file, "r") as reads:
            sqlScript = reads.read()
            cursor_cnxn_msql = self.cnx_mysql.cursor()
            cursor_cnxn_msql.execute(sqlScript)

    def ingest(self, values:dict):
        if values['state'] != 'TOTAL':
            insert_query = self.query_por_estado.format(**values)
        else:
            insert_query = self.query_totais.format(**values)
        
        cursor_cnxn_msql = self.cnx_mysql.cursor()
        cursor_cnxn_msql.execute(insert_query)
        self.cnx_mysql.commit()
