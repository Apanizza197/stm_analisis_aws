import psycopg2
import csv

def process_data(csv_name):
    print("HOLA")
    with open(csv_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for i, row in enumerate(csvreader):
            print(row)
            if i >= 2:
                break
        
def connect_to_database():
    # Set the database connection details
    host = 'pg-stm.cxvntydrp67z.us-east-1.rds.amazonaws.com'
    database = 'stmdb'
    user = 'postgres'
    password = 'AWSC0urs3#UM'

    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    return conn

def import_other_tables(csv_file_name):

    # Connect to the database
    conn = connect_to_database()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the CSV file and iterate over its rows
    with open(csv_file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        start = 50000
        passing = 100000
        for row in reader:
            i = i + 1
            if (i == passing+start): break
            elif(i%10000 == 0): conn.commit()
            elif(i<start):
                pass
            else:
                # Insert values into the tipo_viaje table
                tipo_viaje_values = (row['tipo_viaje'], row['descripcion_tipo_viaje'])
                cur.execute("INSERT INTO viajes_stm.tipo_viaje (tipo_viaje, descripcion) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                            , tipo_viaje_values)

                # Insert values into the grupo_usuario table
                grupo_usuario_values = (row['grupo_usuario'], row['descripcion_grupo_usuario'])
                cur.execute("INSERT INTO viajes_stm.grupo_usuario (grp_usuario, descripcion) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                            , grupo_usuario_values)

                # Insert values into the grupo_usuario_especial table
                grupo_usuario_especial_values = (row['grupo_usuario_especifico'], row['descripcion_grupo_usuario_espe'])
                cur.execute("INSERT INTO viajes_stm.grupo_usuario_especial (grp_usuario_esp, descripcion) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                           , grupo_usuario_especial_values)
        
                # Insert values into the empresa table
                empresa_values = (row['cod_empresa'], row['descrip_empresa'])
                cur.execute("INSERT INTO viajes_stm.empresa (cod_empresa, descripcion) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                            , empresa_values)

                # Insert values into the linea table
                linea_values = (row['linea_codigo'], row['dsc_linea'])
                cur.execute("INSERT INTO viajes_stm.linea (codigo_linea, descripcion) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                            , linea_values)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()

def import_viajes_tables(csv_file_name):    
    # Connect to the database
    conn = connect_to_database()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the CSV file and iterate over its rows
    with open(csv_file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        start = 0
        passing = 100000
        for row in reader:
            i = i + 1
            if (i == passing+start): break
            elif(i<start):
                pass
            elif(i%10000 == 0): conn.commit()
            else:
                # Insert values into the viaje_stm table
                viaje_stm_values = (row['id_viaje'], row['con_tarjeta'], row['fecha_evento'], row['tipo_viaje'], row['grupo_usuario'], 
                    row['grupo_usuario_especifico'], row['ordinal_de_tramo'], row['cantidad_pasajeros'], row['codigo_parada_origen'], 
                    row['cod_empresa'], row['linea_codigo'], row['sevar_codigo'])
                cur.execute("""INSERT INTO viajes_stm.viaje_stm
                (id_viaje, con_tarjeta, fecha_evento, tipo_viaje, grp_usuario, grp_usuario_esp, ordinal_tramo, cant_pasajeros, codigo_parada, co>
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING"""
                            , viaje_stm_values)
    conn.commit()
    cur.close()
    conn.close()
