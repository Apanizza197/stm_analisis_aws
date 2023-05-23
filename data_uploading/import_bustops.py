import psycopg2
import csv

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

def import_bus_table(csv_file_name):

    # Connect to the database
    conn = connect_to_database()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the CSV file and iterate over its rows
    with open(csv_file_name, newline='', delimiter = ';') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        start = 0
        for row in reader:
            i = i + 1
            if(i%10000 == 0):
                print("Commiting to the database, uploading other tables")
                print(f"Reading line {i}")
                conn.commit()
            if(i<start):
                pass
            else:
                # Insert values into the tipo_viaje table
                bustop_values = (row['COD_UBIC_PARADA'], row['DESC_LINEA'], row['COD_VARIAN'],
                                 row['ORDINAL'], row['CALLE'], row['ESQUINA'], row['COD_CALLE1'],
                                 row['COD_CALLE2'], row['COORD_X'], row['COORD_Y'])
                cur.execute("""INSERT INTO viajes_stm.tipo_viaje (tipo_viaje, descripcion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                            , bustop_values)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()


#csv_name = "csv_files/vptu" #TODO CAMBIAR ESTO
#process_data(csv_name)

import_bus_table("csv_files/viajes_stm_012023.csv")






