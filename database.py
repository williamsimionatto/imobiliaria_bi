import psycopg2
import pandas as pd

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="imobiliaria",
        password="imobiliaria",
        port="5432"
    )

    return conn

def close(conn):
    conn.close()

def insert(con, sql):
  cur = con.cursor()

  try:
    cur.execute(sql)
    con.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print("Error: %s" % error)
    con.rollback()
    cur.close()
    return 1

  cur.close()

