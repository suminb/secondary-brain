from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from brain.models import Base, Market, Symbol
import click


DEFAULT_DB_URI = 'sqlite:///default.db'


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
    """Creates an empty database and tables."""
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
    """Manually inserts a market entity to the database."""
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
    """Imports symbols from a text file which contains one symbol per line."""
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


if __name__ == '__main__':
    cli()
