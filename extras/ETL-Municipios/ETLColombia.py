import io
import json
import time
import psycopg2
import sys, os
#Variables gobables
error_con = False
#Parámetros de conexion
v_host = ""
v_port = ""
v_database = ""
v_user = ""
v_password = ""

#---------------------------------------------------------------------------------------------------------------
#CONEXIÓN A BD
#---------------------------------------------------------------------------------------------------------------
tiempo_inicial = time.time()
try:
    connection = psycopg2.connect(user= v_user, password=v_password, host= v_host,
                                  port= v_port, database= v_database)
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Estás conectado a - ", record, "\n")
except (Exception) as error:
    print("Error: ", error)
    error_con = True
finally:
    if (error_con):
        print("Error de conexión con servidor PostgreSQL")
#---------------------------------------------------------------------------------------------------------------
#Cargar tabla
#--------------------------------------------------------------------------------------------------------------- 
def cargarDepartamentosYMunicipios(connection, cursor, contador, departamento, pais_id):
    print(f"Cargando departamento ---> {departamento['departamento']} registro #{contador+1}")
    try:
        command = '''INSERT INTO main_departamento(id, description, pais_id) VALUES(%s, %s, %s)'''
        cursor.execute(command, (departamento['id'], departamento['departamento'], pais_id))
        connection.commit()
        for ciudad in departamento['ciudades']:
            print(f"cargando ciudad -> {ciudad}")
            command= '''INSERT INTO main_municipio(description, departamento_id) VALUES(%s, %s)'''
            cursor.execute(command, (ciudad, departamento['id']))
            connection.commit()
            
    except(Exception) as error:
        print(f"Error cargando la tabla: {error}, {contador}, {departamento['departamento']}")
#---------------------------------------------------------------------------------------------------------------
#Limpieza de tablas 
#---------------------------------------------------------------------------------------------------------------
command = '''TRUNCATE main_departamento CASCADE'''
cursor.execute(command)
command = '''TRUNCATE main_municipio CASCADE'''
cursor.execute(command)
command = '''ALTER SEQUENCE main_municipio_id_seq RESTART WITH 1'''
cursor.execute(command)

#---------------------------------------------------------------------------------------------------------------
#Abrir el archivo JSON de los datos
#---------------------------------------------------------------------------------------------------------------
try:
    archivo = "C:\\Users\swan5\\Desktop\\universidad\\projects\\arriendofinca\\extras\\ETL-Municipios\\Colombia.json"
    with io.open(archivo, encoding=('utf-8')) as f:
        data = json.load(f)
        #ID PAIS
        pais_id = 1
                
        contador = 0
        registro = 0
        
        for item in data:
            cargarDepartamentosYMunicipios(connection, cursor, contador, item, pais_id)
            contador += 1

            
except (Exception) as error:
    print(f"Error leyendo el archivo JSON ------------> {error}")
finally:
    if(connection):
        connection.close()
        print(f"Conexion con la base de datos {v_database} cerrada.")
        

    
tiempo_final = time.time()
tiempo_total_transcurrido = tiempo_final - tiempo_inicial
tiempo_dos_decimales = round(tiempo_total_transcurrido, 2)

print(f"Fin del proceso ETL.\nTiempo de ejecucion: {tiempo_dos_decimales} segundos.")