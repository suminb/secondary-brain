from stock.models import Granularity
from datetime import datetime
import requests
import urllib
import json


class Fetcher(object):
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def fetch_url(url: str, headers: dict) -> str:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise Exception('{}: {}'.format(str(resp), resp.text))

        return resp.text

    def fetch(self, symbol: str, begin_datetime: datetime,
              end_datetime: datetime, granularity: str):
        raise NotImplementedError()


class YahooFetcher(Fetcher):
    @staticmethod
    def build_url(symbol: str, begin_datetime: datetime,
              end_datetime: datetime, granularity: str):

        query_string = json.dumps(dict(s=symbol + '+Interactive'))
        return 'http://finance.yahoo.com/_td_charts_api/resource/' \
               'charts;comparisonTickers=;events=div%7Csplit%7Cearn;' \
               'gmtz=9;indicators=quote;period1={};period2={};' \
               'queryString=%7B%22s%22%3A%22{}%2BInteractive%22%7D;' \
               'range=1d;rangeSelected=undefined;ticker={};' \
               'useMock=false'.format(
            begin_datetime.strftime('%s'), end_datetime.strftime('%s'),
            urllib.parse.quote_plus(query_string), urllib.parse.quote_plus(symbol)
        )

    def get_range(self, granularity: Granularity):
        # TODO: Check if granularity is valid
        return None

    def fetch(self, symbol: str, begin_datetime: datetime,
              end_datetime: datetime, granularity: str):
        url = self.build_url(symbol, begin_datetime, end_datetime, granularity)

        self.logger.info('Fetching {}'.format(url))

        headers = {
            'Content-Type': 'application/json',
            'Referer': 'http://finance.yahoo.com/echarts?s={}+Interactive'.format(urllib.parse.quote_plus(symbol)),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/40.0.2214.111 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        return self.fetch_url(url, headers)