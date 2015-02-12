from stock.stock_parser import StockParser
from stock.models import Symbol, Ticker
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class Importer(object):
    def __init__(self):
        raise NotImplementedError()

    def import_(self, parser: StockParser) -> None:
        raise NotImplementedError()


class YahooImporter(Importer):
    def __init__(self, session):
        self.session = session

    def import_(self, parser: StockParser) -> None:
        """
        TODO:
        1. if symbol does not exist, register one
        2. execute parser.parse()
        3. insert all data into the database
        :param parser:
        :return:
        """
        query = self.session.query(Symbol).filter(Symbol.symbol == parser.symbol)

        if not self.session.query(query.exists()).scalar():
            symbol = Symbol.create(name='(TO BE FILLED)', symbol=parser.symbol,
                                   session=self.session)
        else:
            symbol = query.first()

        for timestamp, volume, open, close, low, high in parser.quotes:
            try:
                ticker = Ticker.create(
                    symbol=symbol,
                    granularity=parser.granularity,
                    timestamp=datetime.fromtimestamp(timestamp),
                    volume=volume,
                    open=open, close=close,
                    low=low, high=high,
                    session=self.session)

            except IntegrityError:
                self.session.rollback()
