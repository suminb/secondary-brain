from sqlalchemy import Column, Integer, BigInteger, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import click

DEFAULT_DB_URI = 'sqlite:///default.db'
Base = declarative_base()


class Market(Base):
    __tablename__ = 'market'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    #: Represents a region to which this market belongs to (e.g., US, KR)
    region = Column(String)

    description = Column(Text)


class Symbol(Base):
    """This may represents a particular company (e.g., Google, Microsoft, etc.)
    or an index (e.g., S&P 500, KOSPI 200, etc.)"""
    __tablename__ = 'symbol'

    id = Column(Integer, primary_key=True)
    market_id = Column(BigInteger, ForeignKey('market.id'))
    name = Column(String)

    market = relationship('Market', backref=backref('symbols'))


class Ticker(Base):
    __tablename__ = 'ticker'

    id = Column(Integer, primary_key=True)
    symbol_id = Column(BigInteger, ForeignKey('symbol.id'))

    symbol = relationship('Symbol', backref=backref('tickers'))


class Article(Base):
    """Represents a news/blog article"""
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)


def get_engine(db_uri):
    return create_engine(db_uri, echo=False)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
def create_db(db_uri):
    """Creates an empty database and tables."""
    engine = get_engine(db_uri)
    Base.metadata.create_all(engine)


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
@click.option('--market_id', help='Market ID (integer)')
@click.option('--market_name', help='Market name (e.g., Nasdaq)')
def insert_market(db_uri, market_id, market_name):
    """Manually inserts a market entity to the database."""
    session = get_session(get_engine(db_uri))
    market = Market(
                id=market_id,
                name=market_name,
    )
    session.add(market)
    session.commit()


@cli.command()
@click.option('--db-uri', default=DEFAULT_DB_URI, help='Database URI')
@click.option('--market_id', help='Market ID (integer)')
@click.option('--filename', help='File containing symbols')
def import_symbols(db_uri, market_id, filename):
    """Imports symbols from a text file which contains one symbol per line."""
    engine = get_engine(db_uri)
    session = get_session(engine)
    with open(filename, 'r') as fin:
        for line in fin:
            symbol = Symbol(
                        market_id=int(market_id),
                        name=line.strip(),
            )
            session.add(symbol)
        session.commit()

#cli = click.CommandCollection(sources=[create_db_cli, import_symbols_cli])


if __name__ == '__main__':
    cli()
