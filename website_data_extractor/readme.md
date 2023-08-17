# Readme for WebsiteSpider

## Introduction

`WebsiteSpider` é uma classe Spider desenvolvida com a biblioteca Scrapy para raspar números de telefone e URLs de logotipos de um conjunto de sites. A classe Spider raspa os números de telefone da página HTML e também procura pelo logotipo da empresa, caso exista.

## Como Funciona

1. **Extração de Números de Telefone**: A Spider procura por números de telefone em diferentes formatos utilizando expressões regulares. Os números são extraídos e limpos para remover caracteres indesejados.

2. **Encontrar o Logotipo**: A função `find_logo` tenta encontrar o URL do logotipo na página.

3. **Seguir Links**: Se houver links que contêm palavras-chave específicas, como 'contato' ou 'telefone', a Spider segue esses links para encontrar informações adicionais.

## Como Usar

### Construindo a Imagem Docker

1. Construa a imagem Docker com o seguinte comando:

   ```bash
   docker build -t my_spider .
   ```

### Executando a Spider

1. Prepare um arquivo `websites.txt` contendo as URLs dos sites que você deseja raspar.

2. Execute a seguinte linha de comando:

   ```bash
   cat websites.txt | docker run -i -v $(pwd)/output:/app/output my_spider
   ```

Aqui, a opção `-v` monta o diretório de saída para que os resultados raspados sejam armazenados no host.

### Saída

A saída incluirá a URL, o URL do logotipo (se encontrado) e os números de telefone extraídos, em formato JSON.

## Considerações

- A Spider está configurada para funcionar especificamente com os padrões de números de telefone e logotipos encontrados nos sites de destino. Pode ser necessário personalizar as expressões regulares ou os métodos de extração para sites diferentes.

- Este projeto assume que os sites são públicos e permitem web scraping de acordo com seus termos de serviço.

## Contribuição

Sinta-se à vontade para contribuir com este projeto, fazendo fork e enviando pull requests, ou abrindo issues para discutir melhorias e recursos adicionais.