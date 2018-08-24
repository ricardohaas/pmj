import scrapy
import time
from scrapy.selector import Selector

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://transparencia.joinville.sc.gov.br/?p=3.5&registros_pagina=500&inicio=02/01/2018&fim=02/01/2018&cpf_cnpj=382.724.669-53']


    def parse(self, response):
        for list_page in response.css('.tableDados tr'):
            next_url = list_page.css('a ::attr(href)').extract_first()
            if( next_url is not None and "p=3.6" in next_url):
                yield response.follow(next_url, self.parse_list)

    def parse_list(self, response):
        for list_page in response.css('.tableDados tr'):
            next_url = list_page.css('a ::attr(href)').extract_first()
            if( next_url is not None and "p=3.3.1" in next_url):
                yield response.follow(next_url, self.parse_item)



    def parse_item(self, response):
        for item_line in response.css('.tableForm tr'):
            favored = self.parse_item_favored(item_line.extract())
            if( favored is not None):
                print(favored)

        for item_line in response.css('.tableForm tr table tr'):
            institution = self.parse_item_institution(item_line.extract())
            if( institution is not None):
                print(institution)

            function = self.parse_item_common_line(item_line.extract(), 'Função')
            if( function is not None):
                print(function)

            function = self.parse_item_common_line(item_line.extract(), 'Data Emissão')
            if( function is not None):
                print(function)

            function = self.parse_item_common_line(item_line.extract(), 'Licitação')
            if( function is not None):
                print(function)

            function = self.parse_item_common_line(item_line.extract(), 'Unidade Gestora')
            if( function is not None):
                print(function)

            function = self.parse_item_common_line(item_line.extract(), 'Despesa')
            if( function is not None):
                print(function)

            function = self.parse_item_common_line(item_line.extract(), 'Valor empenhado')
            if( function is not None):
                print(function)

            function = self.parse_item_common_line(item_line.extract(), 'Contrato')
            if( function is not None):
                print(function)

    def parse_item_favored(self, item_line ):
        if( "Favorecido" in item_line):
            for favoredText in Selector(text=item_line).css('td::text').extract():
                if( favoredText is not None ):
                    return favoredText.split(' - ')
        return None

    def parse_item_institution(self, item_line ):
        if( "Orgão" in item_line):
            for institutionText in Selector(text=item_line).css('td:nth-child(2)::text').extract():
                if( institutionText is not None ):
                    return institutionText.split('-')
        return None

    def parse_item_common_line(self, item_line, keyword):
        if( keyword in item_line):
            for lineText in Selector(text=item_line).css('td:nth-child(2)::text').extract():
                if( lineText is not None ):
                    return lineText.split('-')
            for lineText in Selector(text=item_line).css('td:nth-child(2) span::text').extract():
                if( lineText is not None ):
                    return lineText.split('-')
        return None
