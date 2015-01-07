import pytest


@pytest.fixture(scope='session')
def testapp():
    """Setup any state specific to the execution of the given module."""
    return None


def test_models():
    from brain.models import Market, Symbol, Ticker
    assert hasattr(Market, 'id')
    assert hasattr(Symbol, 'id')
    assert hasattr(Ticker, 'id')
