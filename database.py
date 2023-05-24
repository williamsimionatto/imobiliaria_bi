import mysql.connector
# import pandas as pd

from dotenv import dotenv_values

config = dotenv_values(".env")

def connect():
  conn = mysql.connector.connect(
    host=config['HOST'],
    user=config['MYSQL_USER'],
    password=config['MYSQL_PASSWORD'],
    database=config['MYSQL_DATABASE']
  )

  return conn

def close(conn):
  conn.close()

def insert(conn, sql):
  cursor = conn.cursor()
  try:
    cursor.execute(sql)
    conn.commit()
    cursor.close()
  except Exception as e:
    print(sql)
    print('Error: {}'.format(e))
    conn.rollback()
  finally:
    cursor.close()

