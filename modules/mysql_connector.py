import mysql.connector
import yaml
import pandas as pd
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
