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

#
> Repositório do trabalho final da disciplina de  Business Intelligence UPF 2023/1.