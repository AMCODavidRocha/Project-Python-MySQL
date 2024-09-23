from modules.mysql_connector import Conexion
path = 'database_connections_project/cred/db_credentials.yaml'

print(">>>>>>>>>>INICIO")

conexion = Conexion(path)

conexion.get_connection()

df= conexion.query("SELECT * FROM actor LIMIT 5")

print(df)

conexion.close_connection()

print("FINAL<<<<<<<<<<")


#read sql en pandas