# Use uma imagem base do Python 3.10
FROM python:3.10-slim

# Defina o diretório de trabalho no container
WORKDIR /usr/src/app

# Copie o arquivo de requisitos para o container
COPY requirements.txt ./

# Instale os pacotes necessários
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o projeto para o container
COPY . .

# Comando para executar o Spider quando o container for iniciado
CMD [ "scrapy", "crawl", "website" ]
