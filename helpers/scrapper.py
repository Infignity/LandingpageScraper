import logging
from bs4 import BeautifulSoup


class BsScrapper:
    '''BS4 extended class scrappers'''
    def __init__(self, web_response):
        '''constructor method for extended Bs4'''
        self.web_response = web_response

    def bs_scrap(self):
        """scrapp or return nothing"""
        try:
            soup = BeautifulSoup(
                self.web_response.text, 
                'html.parser'
            )
            return soup.get_text()
        except AttributeError:
            logging.error(
                f'Response not text: {self.web_response.status} \
                      {self.web_response.headers}'
            )
            soup = BeautifulSoup('')
