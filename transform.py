import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

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


# transform_data()
