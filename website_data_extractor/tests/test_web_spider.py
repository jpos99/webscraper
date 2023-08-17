import os
import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from scrapy.http import TextResponse

from website_data_extractor.website_data_extractor.spiders.web_spider import WebsiteSpider


class TestWebsiteSpider(unittest.TestCase):

    def test_clean_phone_numbers(self):
        assert WebsiteSpider.clean_phone_numbers(["+1 (800) 123-4567"]) == ["+1 (800) 1234567"]

        assert WebsiteSpider.clean_phone_numbers(["AB+1 (800) 123-4567CD"]) == ["+1 (800) 1234567"]

        assert WebsiteSpider.clean_phone_numbers([]) == []

        assert WebsiteSpider.clean_phone_numbers(["  +1 (800) 123-4567  "]) == ["+1 (800) 1234567"]

    def test_parse(self):

        html_body = '''<html>
            <body>
                <img src="//s26.q4cdn.com/888045447/files/design/ClientLogo.png" id="_ctrl0_ctl24_img1" border="0" alt="Homepage">
                <p>Contact: +1234567890</p>
            </body>
        </html>'''
        response = TextResponse(url="http://example.com", body=html_body, encoding='utf-8')

        spider = WebsiteSpider(file_path="some_file.txt")

        result = next(spider.parse(response))

        expected_result = {
            'url': "http://example.com",
            'logo': "https://s26.q4cdn.com/888045447/files/design/ClientLogo.png",
            'phone_numbers': ["+1234567890"]
        }
        self.assertEqual(result, expected_result)

    def test_find_logo(self):
        html_body = '<html><body><img src="//s26.q4cdn.com/888045447/files/design/ClientLogo.png" id="_ctrl0_ctl24_img1" border="0" alt="Homepage"></body></html>'
        response = TextResponse(url="http://example.com", body=html_body, encoding='utf-8')
        logo_url = WebsiteSpider.find_logo(response)
        expected_logo_url = "https://s26.q4cdn.com/888045447/files/design/ClientLogo.png"
        self.assertEqual(logo_url, expected_logo_url)


if __name__ == '__main__':
    unittest.main()




