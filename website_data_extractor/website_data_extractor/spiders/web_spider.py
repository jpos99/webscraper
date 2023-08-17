import re
import sys

import scrapy
from scrapy.selector import Selector


class WebsiteSpider(scrapy.Spider):
    Selector._DEFAULT_NAMESPACES = {
        're': 'http://exslt.org/regular-expressions'
    }
    name = 'website'
    start_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not sys.stdin.isatty():
            domains = sys.stdin.readlines()
            self.start_urls = [domain.strip() for domain in domains]
        else:
            self.start_urls = []

    @staticmethod
    def clean_phone_numbers(phone_numbers):
        return [''.join(filter(lambda x: x.isdigit() or x in ["(", ")", "+", " "], num)).strip() for num in phone_numbers]

    @staticmethod
    def extract_phone_numbers(response):

        page_text = response.xpath('//text()').getall()
        page_text = " ".join(page_text)

        candidate_numbers = []
        candidate_numbers += re.findall(r'\(?\+?[0-9]{1,3}\)?\s*\(?[0-9]{1,7}\)?[-.\s]*[0-9]{1,7}[-.\s]*[0-9]{1,7}', page_text)
        candidate_numbers += re.findall(r'\+\d{2}\s\d\s\d{4}\s\d{4}', page_text)
        candidate_numbers += re.findall(r'\b0800\s\d{6}\b', page_text)
        candidate_numbers += re.findall(r'\+\d{2}\s\d\s\d{4}\s\d{4}', page_text)
        candidate_numbers += re.findall(r'\b1800\s\d{3}\s\d{3}\b', page_text)
        candidate_numbers += re.findall(r'\+\d\s\(\d{3}\)\s\d{3}-\d{4}', page_text)
        candidate_numbers += re.findall(r'\+\d\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}', page_text)

        page_phones = [link for link in response.xpath('//a/@href').extract() if link.startswith("tel:")]
        page_phones_numbers = [phone_number.replace('tel:', '') for phone_number in page_phones]

        specific_patterns = [
            r'^\d{2} \d{2} \d{2}$',
            r'^0800 \d{6}$',
            r'^\+\d{2} \d \d{4} \d{4}$',
            r'^1800 \d{3} \d{3}$',
            r'^\+\d \(?\d{3}\)? \d{3}-\d{4}$',
            r'^\+\d \(?\d{3}\)? \d{3}-\d{2}-\d{2}$',
            r'^\(\d{3}\) \d{3}-\d{4}$',
            r'^\+\d \d{3}-\d{3}-\d{4}$',
            r'^\+\d{3} \d{7}$',
            r'^\+\d{2} \d{2} \d{4} \d{3}$'
        ]
        filtered_numbers = [num for num in candidate_numbers if
                            any(re.match(pattern, num) and num != '' for pattern in specific_patterns)]
        filtered_numbers += [num for num in page_phones_numbers if
                            any(re.match(pattern, num) and num != '' and num.replace(' ', '') not in filtered_numbers for pattern in specific_patterns)]

        return set(filtered_numbers)

    def parse(self, response):

        keywords = ['contact', 'phone']

        for link in response.css('a::attr(href)').extract():
            for keyword in keywords:
                if keyword in link:
                    url = response.urljoin(link)
                    yield scrapy.Request(url, callback=self.extract_phone_numbers)
        logo_url = self.find_logo(response)
        phone_numbers = self.extract_phone_numbers(response)
        cleaned_numbers = set(self.clean_phone_numbers(phone_numbers))

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
