import pandas as pd
import database as db

def transform_data():
  sales = pd.read_csv('./data/dataset-Venda.csv', sep=';')
  rents = pd.read_csv('./data/dataset-Alguel.csv', sep=';')

  sales['transaction_type'] = 'Venda'
  rents['transaction_type'] = 'Alguel'

  sales['garage'] = sales['garage'].apply(lambda x: x.replace('parking', ''))
  rents['garage'] = rents['garage'].apply(lambda x: x.replace('parking', ''))

  dataset = pd.concat([sales, rents])

  dataset.to_csv('./data/dataset.csv', sep=';', index=False, encoding='utf-8-sig')


def insert_types(conn):
  types = pd.DataFrame({
    'name': ['Kitnet', 'Apartamento', 'Casa de Condomínio', 'Studio', 'Vila', 'Casa', 'Loft', 'Terreno', 'Outros'],
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9]
  })

  for index, row in types.iterrows():
    sql = "INSERT INTO property_type (id, name) VALUES ({}, '{}')".format(row['id'], row['name'])
    db.insert(conn, sql)


def insert_properties(conn):
  dataset = pd.read_csv('./data/dataset.csv', sep=';')

  for index, row in dataset.iterrows():
    if pd.isnull(row['address']):
      row['address'] = ''

    if pd.isnull(row['neighborhood/city']):
      row['neighborhood/city'] = ''
  
    row['address'] = row['address'].replace("'", "")
    row['neighborhood/city'] = row['neighborhood/city'].replace("'", "")

    sql = "INSERT IGNORE INTO real_estate (price, address, neighborhood_city, rooms, garage, bathroom, square_meter, type_id, suite, gym, balcony, hall, transaction_type) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}')".format(
        row['price'],
        row['address'],
        row['neighborhood/city'],
        int(row['rooms']),
        int(row['garage']),
        int(row['bathroom']),
        float(row['square_meter']),
        int(row['type']),
        bool(row['suite']),
        bool(row['gym']),
        bool(row['balcony']),
        bool(row['hall']),
        str(row['transaction_type'])
      )

    db.insert(conn, sql)


def save_data():
  conn = db.connect()
  insert_types(conn)
  insert_properties(conn)

  db.close(conn)


transform_data()

save_data()
