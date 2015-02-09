from brain.stock_parser import StockParser
from brain.models import Symbol, Ticker


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

        if not self.session.query(query.exists()):
            pass

        for timestamp, volume, open, close, low, high in parser.quotes:
            print(timestamp, volume, open, close, low, high)