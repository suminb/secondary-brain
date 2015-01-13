# -*- coding: utf-8 -*-
from brain.stock_parser import StockParser
import json

class YahooStockParser(StockParser):
    def __init__(self):
        self.__symbol = None

    def load(self, filepath):
        raw_objects = self.load_raw_objects(filepath)
        meta = raw_objects['data']['meta']
        quotes = raw_objects['data']['indicators']['quote']

        self.__symbol = meta['symbol']

    def load_raw_objects(self, filepath):
        with open(filepath) as fin:
            return json.loads(fin.read())

    @property
    def symbol(self):
        return self.__symbol


# For debugging purposes
if __name__ == '__main__':
    parser = YahooStockParser()
    parser.load('tmp/035720.KQ.txt')