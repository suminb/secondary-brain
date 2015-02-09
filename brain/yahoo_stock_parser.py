# -*- coding: utf-8 -*-
from brain.stock_parser import StockParser
import json

class YahooStockParser(StockParser):
    def __init__(self):
        self.__symbol = None
        self.meta = None

    def load(self, filepath):
        raw_objects = self.load_raw_objects(filepath)
        self.meta = raw_objects['data']['meta']
        self.__quotes = self.load_quotes(raw_objects['data']['timestamp'],
                                         raw_objects['data']['indicators']['quote'])

        self.__symbol = self.meta['symbol']

    def load_raw_objects(self, filepath):
        with open(filepath) as fin:
            return json.loads(fin.read())

    def load_quotes(self, timestamps: list, raw: list):
        # FIXME: Deal with cases where len(raw) > 1
        r = raw[0]

        keys = ('volume', 'open', 'close', 'low', 'high')
        volumes, opens, closes, lows, highs, = map(lambda k: r[k], keys)

        return zip(timestamps, volumes, opens, closes, lows, highs)

    @property
    def symbol(self):
        return self.__symbol

    @property
    def quotes(self):
        return self.__quotes

    @property
    def granularity(self):
        return self.meta['dataGranularity']


# For debugging purposes
if __name__ == '__main__':
    parser = YahooStockParser()
    parser.load('tmp/035720.KQ.txt')

    print(parser.granularity)