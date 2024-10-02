from modules.mysql_connector import Conexion
from modules.mysql_connector import Conexion_cdb
path = 'database_connections_project/cred/db_credentials.yaml'

opcion = input("MySQL/CouchDB [M/C?]").lower()
if opcion == "m":
    print(">>>>>>>>>>MySQL")

    conexion = Conexion(path)

    conexion.get_connection()

    df= conexion.query("SELECT * FROM actor LIMIT 5")

    print(df)

    conexion.close_connection()

    print("MySQL<<<<<<<<<<")

elif opcion == "c":
    print(">>>>>>>>>>CouchDB")
    print("CONEXION:")
    conexion = Conexion_cdb(path)

    conexion.get_connection("personas")

    mango_query = {
        "selector": {
        "direccion.ciudad": {
           "$regex": "(?i)pan"
        }
        },
        "fields": [
             "nombre",
            "apellido",
            "edad"
        ],
        "sort": [
            {
                "edad": "asc"
            }
        ],
        "limit":3
    }
    print("MANGO QUERY!!")
    r = conexion.mango(mango_query)
    for doc in r:
        print(f"Doc: {doc}")
    print("VISTA QUERY!!")
    r = conexion.vista('datosPersonas/edad-ordenada')
    for fila in r:
        print(fila.key, fila.value)

    print("CouchDB<<<<<<<<<<")
else:
    print("Opcion incorrecta...")