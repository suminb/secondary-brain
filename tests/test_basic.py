# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope='session')
def testapp():
    """Setup any state specific to the execution of the given module."""
    return None


def test_models():
    from stock.models import Market, Symbol, Ticker
    assert hasattr(Market, 'id')
    assert hasattr(Symbol, 'id')
    assert hasattr(Ticker, 'id')


def test_commands():
    from click.testing import CliRunner
    from stock.bin import DEFAULT_DB_URI, get_engine, get_session, create_db, \
        insert_market

    engine = get_engine(DEFAULT_DB_URI)
    assert engine is not None

    session = get_session(engine)
    assert session is not None

    runner = CliRunner()
    runner.invoke(create_db, [DEFAULT_DB_URI])
    runner.invoke(insert_market, [DEFAULT_DB_URI, 1, 'NASDAQ'])
