# -*- coding: utf-8 -*-
from stock.fetcher import YahooFetcher
from datetime import datetime, timedelta
from logbook import Logger
import json

logger = Logger(__file__)


def test_fetcher():
    fetcher = YahooFetcher(logger=logger)
    raw_data = fetcher.fetch('AAPL', datetime.now() - timedelta(days=365),
                             datetime.now(), '1day')

    objects = json.loads(raw_data)

    assert type(objects) == dict