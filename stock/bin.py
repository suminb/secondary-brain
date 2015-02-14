# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stock.models import Base, Market, Symbol
from stock.importer import YahooImporter
from stock.stock_parser import YahooStockParser
from stock.fetcher import YahooFetcher
from datetime import datetime, timedelta
from logbook import Logger
import click


DEFAULT_DB_URI = 'sqlite:///default.db'
log = Logger(__file__)


def get_engine(db_uri):
    return create_engine(db_uri, echo=False)


def get_session(engine):
    return sessionmaker(bind=engine)()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
def create_db(db_uri):
    """Create an empty database and tables."""
    engine = get_engine(db_uri)
    Base.metadata.create_all(engine)


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
@click.option('--market_id', help='Market ID (integer)')
@click.option('--market_name', help='Market name (e.g., Nasdaq)')
@click.option('--open', required=True,
              help='Time at which the market opens (e.g., 570 for 9:30)')
@click.option('--close', required=True,
              help='Time at which the market closes (e.g., 900 for 15:00)')
def insert_market(db_uri, market_id, market_name, open, close):
    """Manually insert a market entity to the database."""
    assert 0 <= int(open) < 60 * 24
    assert 0 <= int(close) < 60 * 24

    session = get_session(get_engine(db_uri))
    market = Market(
        id=market_id,
        name=market_name,
        open=open,
        close=close,
    )
    session.add(market)
    session.commit()


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
@click.option('--market-id', required=True, help='Market ID (integer)')
@click.option('--filename', required=True, help='File containing symbols')
def import_symbols(db_uri, market_id, filename):
    """Import symbols from a text file which contains one symbol per line."""
    engine = get_engine(db_uri)
    session = get_session(engine)
    with open(filename, 'r') as fin:
        for line in fin:
            symbol = Symbol(
                market_id=int(market_id),
                symbol=line.strip(),
            )
            session.add(symbol)
        session.commit()



@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
@click.option('-f', '--filename', required=True, help='JSON file path')
def import_tickers(db_uri, filename):
    """Import tickers from a JSON file."""
    session = get_session(get_engine(db_uri))
    parser = YahooStockParser()
    parser.load(filename)
    importer = YahooImporter(session)
    importer.import_(parser)


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
@click.option('-s', '--symbol', required=True, help='Symbol')
@click.option('-g', '--granularity', required=True, help='Data granularity')
def fetch(db_uri, symbol, granularity):
    fetcher = YahooFetcher(logger=log)
    raw_data = fetcher.fetch(symbol, datetime.now() - timedelta(days=1), datetime.now(), granularity)

    parser = YahooStockParser(logger=log)
    parser.load(raw_data)

    session = get_session(get_engine(db_uri))
    importer = YahooImporter(session=session, logger=log)
    importer.import_(parser)


if __name__ == '__main__':
    cli()
