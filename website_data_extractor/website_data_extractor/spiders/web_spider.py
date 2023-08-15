import os
import re
import scrapy
from scrapy import Selector


class WebsiteSpider(scrapy.Spider):
    Selector._DEFAULT_NAMESPACES = {
        're': 'http://exslt.org/regular-expressions'
    }
    name = 'website'
    start_urls = []

    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if os.path.exists(file_path):
            self.start_urls = self.create_domain_list_from_file(file_path)
        else:
            self.start_urls = []

    @staticmethod
    def clean_phone_numbers(phone_numbers):
        return [''.join(filter(lambda x: x.isdigit() or x in ["(", ")", "+"], num)).strip() for num in phone_numbers]

    @staticmethod
    def create_domain_list_from_file(file_path):
        with open(file_path, 'r') as domains_file:
            return domains_file.readlines()

    def parse(self, response):
        logo_url = self.find_logo(response)
        body_text = response.text
        phone_numbers = re.findall(r'[+(]?[1-9][0-9 .\-()]{8,}[0-9]', body_text)
        cleaned_numbers = self.clean_phone_numbers(phone_numbers)
        yield {
            'url': response.url,
            'logo': logo_url,
            'phone_numbers': cleaned_numbers
        }

    @staticmethod
    def find_logo(response):
        logo_url = response.xpath('//img/@src').get()
        if logo_url:
            if logo_url.startswith('//'):
                logo_url = 'https:' + logo_url
            return logo_url
        return None
