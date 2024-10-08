import mysql.connector
import couchdb
import yaml
import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
class Conexion:
    
    def __init__ (self, path):
            with open(path) as file:
                yamll = yaml.safe_load(file)

            self.host = yamll['mysql']['host']
            self.port = yamll['mysql']['port']
            self.user = yamll['mysql']['user']
            self.pw   = yamll['mysql']['password']
            self.db   = yamll['mysql']['database']
            self.conector = ""
            self.cursor = ""

    def get_connection(self):
        self.conector = mysql.connector.connect(user=self.user,
                                password=self.pw,
                                port=self.port,
                                database=self.db,
                                host=self.host)
        self.cursor = self.conector.cursor()
    
    def query(self, query):
        self.cursor.execute(query)
        df = pd.DataFrame(self.cursor.fetchall())
        return df
    
    def close_connection(self):
        self.cursor.close()
        self.conector.close()

class Conexion_cdb:
    def __init__ (self, path):
        with open(path) as file:
            yamll = yaml.safe_load(file)
        system = os.name
        if system == "nt":    
            self.user = yamll['couchdbW']['user']
            self.pw = yamll['couchdbW']['password']
            self.couch =  couchdb.Server(f'http://{self.user}:{self.pw}@127.0.0.1:5984/')
            self.db =""
        else:
            self.user = yamll['couchdbM']['user']
            self.pw = yamll['couchdbM']['password']
            self.couch =  couchdb.Server(f'http://{self.user}:{self.pw}@127.0.0.1:5984/')
            self.db =""

    def get_connection(self,db):
        if db in self.couch:
            self.db = self.couch[db]
            print(f"Accediendo a la base de datos '{self.db}'")
        else:
            db = self.couch.create('personas')
            print(f'Base creada: {db}')
    
    def mango(self, mango_query):
        r = self.db.find(mango_query)
        return r
    
    def vista(self, vista):
        r = self.db.view(vista)
        return r
    
class Conexion_bq:
    def __init__ (self):
        apath = "/Users/davidrocha/Desktop/AMCO/database_connections_project/cred/keys.json"
        rpath = "/database_connections_project/cred/keys.json"
        self.path = apath
        self.creds = service_account.Credentials.from_service_account_file(self.path)
        self.client = bigquery.Client(credentials = self.creds, project = self.creds.project_id)

    def bigquery(self):
        bg_query = 'SELECT id, nombre FROM training_bq.personas'
        rquery = self.client.query(bg_query) 
        df = rquery.to_dataframe()
        df.set_index('id', inplace=True)
        return df