from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas as pd
import re
import random

def extract_data(transaction_type, pages):
  cards = []
  garage = []
  headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

  for i in range(pages):
    uri = "https://www.zapimoveis.com.br/venda/?pagina="+str(i)+"&tipo=Im%C3%B3vel%20usado&transacao="+transaction_type
    request = Request(uri, headers = headers)

    try:
      print('Extracting page ' + str(i) + ' --- Transaction: ' + transaction_type)

      response = urlopen(request)
      html = response.read().decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')
    except HTTPError as e:
      print(e.status(), e.reason())
    except URLError as e:
      print(e.reason())

    adverts = soup.find('div',{'class':'listings__container'}).findAll('div',class_='card-listing simple-card')

    for advert in adverts:
      card = {}

      card['id'] = random.randint(0, 1000000)

      price = advert.find('p', {'class': 'simple-card__price js-price color-darker heading-regular heading-regular__bolder align-left'})
      if price is not None:
        card['price'] = int(
                price.get_text()
                .replace(' ', '')
                .replace('R$','')
                .replace('\n','')
                .replace('.','')
                .replace('/mês', '')
                .replace('/dia', '')
                .replace('/semana', '')
                .replace('/ano', '')
              )
      else:
        card['price'] = 0

      address = advert.find('h2',{'class':'simple-card__address color-dark text-regular'})
      if address == None:
        card['address'], card['neighborhood/city'] = str('None'), str('None')
      else :
        card['address'], card['neighborhood/city'], *others = address.get_text().replace('\n','').replace('  ','').split(',')

      rooms = advert.find('span',{'itemprop':'numberOfRooms'})
      if rooms == None:
        card['rooms'] = int(1)
      else :
        card['rooms'] = int(rooms.get_text().replace(' ','').replace('\n',''))

      garage = advert.find('li',{'class':'feature__item text-small js-parking-spaces'})
      if garage == None:
        card['garage'] = int(0)
      else :
        card['garage'] = garage.get_text().replace(' ','').replace('\n','')

      bathroom = advert.find('span',{'itemprop':'numberOfBathroomsTotal'})
      if bathroom == None:
        card['bathroom'] = int(1)
      else :
        card['bathroom'] = int(bathroom.get_text().replace(' ','').replace('\n',''))

      square_meter = advert.find('span',{'itemprop':'floorSize'})
      if square_meter == None:
        card['square_meter'] = int(30)
      else :
        card['square_meter'] = int(square_meter.get_text().replace(' ','').replace('\n','').replace('m²',''))

      description = advert.find('span',{'class':'simple-card__text text-regular'})
      if description == None:
        description = ''
      else :
        description = str(description.get_text().replace('-',' ').replace('\n',''))

      if re.search("kitnet|kitnets|kit|kit net|kitinete|kitinetes|quitinete|kitão|germinada|geminada|conjugado", description.lower()):
        card['type'] =  int(1)
      elif re.search("apartamento|apartamentos|apto|cobertura", description.lower()):
        card['type'] = int(2)
      elif re.search("casa de condominio|casa de condomínio|casa de condominios|casa de condomínios", description.lower()):
        card['type'] =  int(3)
      elif re.search("studio|studios", description.lower()):
        card['type'] =  int(4)
      elif re.search("vila|villa", description.lower()):
        card['type'] =  int(5)
      elif re.search("casa|casas", description.lower()):
        card['type'] =  int(6)
      elif re.search("loft|duplex|dupllex", description.lower()):
        card['type'] =  int(7)
      elif re.search("loteamento|lote|terrenos|terreno|trrno|lote/terreno", description.lower()):
        card['type'] =  int(8)
      else:
        card['type'] =  int(9)

      if re.search("suite|suíte|suites|suítes", description.lower()) != None:
        card['suite'] =  int(1)
      else:
        card['suite'] =  int(0)

      if re.search("academia|academias", description.lower()) != None:
        card['gym'] =  int(1)
      else:
        card['gym'] =  int(0)

      if re.search("varanda|terraço|terraco|sacada|varandas|terraços|terracos|sacadas", description.lower()) != None:
        card['balcony'] =  int(1)
      else:
        card['balcony'] =  int(0)

      if re.search("salao|salão", description.lower()) != None:
        card['hall'] =  int(1)
      else:
        card['hall'] =  int(0)

      cards.append(card)

  dataset = pd.DataFrame(cards)
  dataset.to_csv('./data/dataset-'+transaction_type+'.csv', index=False, sep=';', encoding='utf-8-sig')

NUMBER_OF_PAGES = 10
extract_data('Venda', NUMBER_OF_PAGES)
extract_data('Alguel', NUMBER_OF_PAGES)
