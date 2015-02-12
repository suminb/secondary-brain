from datetime import datetime
import requests


class Fetcher(object):
    @staticmethod
    def fetch_url(url: str) -> str:
        return requests.get(url).text

    def fetch(self, symbol: str, begin_datetime: datetime,
              end_datetime: datetime, granularity: str):
        raise NotImplementedError()


class YahooFetcher(Fetcher):
    def build_url(self, symbol: str, begin_datetime: datetime,
              end_datetime: datetime, granularity: str):
        return 'http://finance.yahoo.com/_td_charts_api/resource/charts;comparisonTickers=;events=div%7Csplit%7Cearn;gmtz=9;indicators=quote;period1=1423235964;period2=1423581564;queryString=%7B%22s%22%3A%22%255EGSPC%2BInteractive%22%7D;range=1d;rangeSelected=undefined;ticker=%5EGSPC;useMock=false?crumb=IDgMckfD8fH'

    def fetch(self, symbol: str, begin_datetime: datetime,
              end_datetime: datetime, granularity: str):
        url = self.build_url(symbol, begin_datetime, end_datetime, granularity)
        self.fetch_url(url)