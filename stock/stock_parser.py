# -*- coding: utf-8 -*-
"""Provides an interface for stock parsers."""
import json


class StockParser(object):
    # FIXME: These properties probably should be under a difference class.
    # For example, StockQuote or something like that.
    @property
    def symbol(self):
        """Stock symbol (e.g., AMZN, YHOO, 035720.KQ)"""
        raise NotImplementedError()

    @property
    def trading_periods(self):
        """A list of trading periods (may be more than one)"""
        raise NotImplementedError()

    @property
    def granularity(self):
        """Data granularity (e.g., 1 sec, 1 min, 1 day, etc.)"""
        raise NotImplementedError()

    @property
    def quotes(self):
        """A list of (datetime, volume, open, close, low, high) tuples"""
        raise NotImplementedError()


class YahooStockParser(StockParser):
    def __init__(self, logger):
        self.__symbol = None
        self.__quotes = None
        self.meta = None
        self.logger = logger

    def load(self, raw_data: str):
        raw_objects = json.loads(raw_data)
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
        mappings = {
            '1m': '1min',
            '5m': '5min',
        }
        key = self.meta['dataGranularity']

        return mappings[key] if key in mappings else None


# For debugging purposes
if __name__ == '__main__':
    parser = YahooStockParser()
    parser.load('tmp/035720.KQ.txt')

    print(parser.granularity)