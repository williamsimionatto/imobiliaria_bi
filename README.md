# Business Intelligence

O trabalho consiste em realizar a extração e transformação de dados sobre imóbiliarias. 

Após a extração e transformação, os dados são carregados em um banco de dados mysql. Para posteriormente serem utilizados em uma ferramenta de visualização de dados.


# Instruções
É necessário ter o docker e docker-compose instalados na máquina.

1. Criar o arquivo `.env` baseado no `.env.example`

2. Rodar o comando para criar o container do banco de dados mysql
```bash
docker-compose up
```

3. Criar as tabelas no banco de dados baseado no arquivo `script.sql`.

4. Rodar o comando para realizar a extração dos dados
```bash
python3 extract.py
```

5. Rodar o comando para realizar a transformação dos dados
```bash
python3 transform.py
```

# Dashboards
Depois de realizar a extração e transformação dos dados, é possível visualizar os dados em dashboards, construídos com a ferramenta [Power BI](https://powerbi.microsoft.com/pt-br/). Os dashboards estão disponíveis no arquivo `imobiliaria.pbix`.

## Dashboard 1

* Mapa com a localização dos imóveis, bem como o seu tipo.
* Filtragem pelo tipo da transação [Venda, Aluguel].

![Maps](./imgs/map.png)

## Dashboard 2
* Gráfico de barras com a média do preço dos imóveis pelo tipo.
* Gráfico de dispersão com a relação entre o número de quartos e a média de banheiros.
* Card com o total de imóveis.
* Card com o preço médio dos imóveis.
* Card com o preço médio dos imóveis por metro quadrado.
* Card com a média de quartos.
* Filtragem por Cidade.
* Filtragem por Tipo de Transação [Venda, Aluguel].
* Filtragem por tipo do imóvel.

![Charts](./imgs/charts.png)

#
> Repositório do trabalho final da disciplina de  Business Intelligence UPF 2023/1.