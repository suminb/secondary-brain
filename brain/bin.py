from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from brain.models import Base, Market, Symbol
import click


DEFAULT_DB_URI = 'sqlite:///default.db'


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
