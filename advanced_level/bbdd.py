import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from pathlib import Path 

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

def bbdd_connection():
    try:
        # Conectar a MySQL Server
        cnx = mysql.connector.connect(
            user = os.getenv('bbdd_user_name'),      
            password = os.getenv('bdd_password'),
            host = os.getenv('bdd_host')  
        )
# ------------------------------------------------------------------------------
        if cnx.is_connected():
            print("Connected to BBDD!")

            mycursor = cnx.cursor()

            mycursor.execute("CREATE DATABASE IF NOT EXISTS bbdd_Taximeter")
            print("Data base 'bbdd_Taximeter' created succesfully.")

            try:
                mycursor.execute("USE bbdd_Taximeter")
                print("Database selected successfully.")
            except mysql.connector.Error as err:
                print("Error selecting the database.")
                print("Error Code", err.errno)
                print("SQLSTATE:", err.sqlstate)
                print("Message:", err.msg)
# ------------------------------------------------------------------------------
    except mysql.connector.Error as err:
        print("An error occurred:")
        print("Error Code:", err.errno)
        print("SQLSTATE:", err.sqlstate)
        print("Message:", err.msg)
# ------------------------------------------------------------------------------
    finally:
        if cnx.is_connected():
            mycursor.close()
            cnx.close()
            print("MySQL connection closed.")
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    bbdd_connection()