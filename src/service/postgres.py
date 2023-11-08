

# import psycopg2
# import pandas as pd
# from sqlalchemy import create_engine, text

# # Define the database connection parameters
# db_params = {
#     'host': 'localhost',
#     'database': 'postgres',
#     'user': 'postgres',
#     'password': 'admin'
# }


# conn = psycopg2.connect(
#     host=db_params['host'],
#     database=db_params['database'],
#     user=db_params['user'],
#     password=db_params['password']
# )

# import csv
# import psycopg2
# conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
# cur = conn.cursor()
# with open('user_accounts.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader) # Skip the header row.
#     for row in reader:
#         cur.execute(
#         "INSERT INTO users VALUES (%s, %s, %s, %s)",
#         row
#     )
# conn.commit()

# import psycopg2
# conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
# cur = conn.cursor()
# cur.execute("""
#     CREATE TABLE users(
#     id integer PRIMARY KEY,
#     email text,
#     name text,
#     address text
# )
# """)

import psycopg2 
from psycopg2.errors import UndefinedTable
import logging
import csv
import os
from src.utils.exceptions import AppException
from src.utils import env

logger = logging.getLogger(env.__LOGGING_NAME__)

def _health():
    print("testing")

def _get_connection(host=None, port=None, database=None, user=None, password=None):
    _host = f"{host if host else env.get_property('postgres', 'host')}"
    _port = port if port else env.get_property('postgres', 'port')
    _db = database if database else env.get_property('postgres', 'database.dbname')
    _user = user if user else env.get_property('postgres', 'database.user')
    _pwd = password if password else env.get_property('postgres', 'database.password')

    logger.debug(f"Getting postgres connector")
    logger.debug(f"   host     [{_host}]")
    logger.debug(f"   port     [{_port}]")
    logger.debug(f"   database [{_db}]")
    logger.debug(f"   user     [{_user}]")

    conn = psycopg2.connect(
        host = _host,
        port = _port,
        database = _db,
        user = _user,
        password = _pwd,
    )
    return conn

def _create_temporary_folder(temporary_folder="tmp"):

    if not os.path.exists(temporary_folder):
        os.makedirs(temporary_folder)

def _get_temporary_file(file_storage, table_name, database):

    logger.debug("Generating temporary file")
    logger.debug(f"    database   [{database}]")
    logger.debug(f"    table_name [{table_name}]")

    temporary_folder = "tmp"
    _create_temporary_folder(temporary_folder=temporary_folder)


    absolut_file_path = f"{temporary_folder}/{database}.{table_name}.csv"

    logger.debug(f"   temporary file path [{absolut_file_path}]")
    file_storage.save(absolut_file_path)
    file_storage.close()

    return open(absolut_file_path, "r")



def load(file_storage, table_name, database, header):

    logger.debug("Initiate the postgres load process")
    logger.debug(f"   database   [{database}]")
    logger.debug(f"   table_name [{table_name}]")
    logger.debug(f"   header     [{header}]")
    tmp_file = _get_temporary_file(file_storage, table_name, database)

    num_lines = len(tmp_file.readlines())
    tmp_file.seek(0)
    lines_limit = int(env.get_property('postgres', 'load.lines_limit', 1000)) 

    logger.debug(f"validating the number of lines that will be loaded")
    logger.debug(f"   files lines [{num_lines}]")
    logger.debug(f"   limit       [{lines_limit}]")

    if num_lines > lines_limit:
        raise AppException(f"It was exceeded the lines limit of the file. The file contains {num_lines} lines and our limit is {lines_limit} lines per file, including the header!", 400)

    conn = _get_connection(database=database)
    cur = conn.cursor()


    if header:
        next(tmp_file)

    try:
        logger.debug(f"loading into postgres")

        cur.copy_from(tmp_file, table_name, sep=',')
        conn.commit()
        
    except UndefinedTable as e:
        raise AppException(e, 400)
    except Exception as e:
        raise AppException(e, 500)
    finally:
        logger.debug(f"closing file and connections")
        tmp_file.close()
        conn.close()
    
    logger.debug(f"loading done")
