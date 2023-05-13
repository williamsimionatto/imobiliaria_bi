import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import database as db

i = 0

def get_lat_long(address):
  global i
  print('Getting lat/long for address ' + str(i))
  i += 1

  geolocator = Nominatim(user_agent="geolocalização")
  geocode = RateLimiter(geolocator, min_delay_seconds=1, return_value_on_exception = None)

  location = geolocator.geocode(address, timeout=None)

  if location == None:
    return (None, None)
  else:
    return (location.latitude, location.longitude)


def transform_data():
  sales = pd.read_csv('./data/dataset-Venda.csv', sep=';')
  rents = pd.read_csv('./data/dataset-Alguel.csv', sep=';')

  sales['transaction_type'] = 'Venda'
  rents['transaction_type'] = 'Alguel'

  sales['lat_long'] = sales['address'] + ', ' + sales['neighborhood/city']
  sales['lat_long'] = sales['lat_long'].apply(get_lat_long)
  sales['lat'] = sales['lat_long'].apply(lambda x: x[0])
  sales['long'] = sales['lat_long'].apply(lambda x: x[1])

  sales.drop('lat_long', axis=1, inplace=True)

  print(sales.head())

  rents['lat_long'] = rents['address'] + ', ' + rents['neighborhood/city']
  rents['lat_long'] = rents['lat_long'].apply(get_lat_long)
  rents['lat'] = rents['lat_long'].apply(lambda x: x[0])
  rents['long'] = rents['lat_long'].apply(lambda x: x[1])
  rents.drop('lat_long', axis=1, inplace=True)

  print(rents.head())

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
    lat = row['lat'] if pd.notnull(row['lat']) else 0
    long = row['long'] if pd.notnull(row['long']) else 0

    sql = "INSERT INTO real_estate (price, address, neighborhood_city, rooms, garage, bathroom, square_meter, type_id, suite, gym, balcony, hall, transaction_type, lat, long) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', {}, {})".format(
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
        str(row['transaction_type']),
        float(lat),
        float(long)
      )

    db.insert(conn, sql)


def save_data():
  conn = db.connect()
  insert_types(conn)
  insert_properties(conn)

  db.close(conn)


# transform_data()

save_data()
