FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["scrapy", "crawl", "website", "-o", "output_file.json"]