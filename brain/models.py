from sqlalchemy import Column, Integer, BigInteger, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Market(Base):
    __tablename__ = 'market'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    #: Represents a region to which this market belongs to (e.g., US, KR)
    region = Column(String)

    #: Denotes time at which the market opens (e.g., 570 for 9:30)
    open = Column(Integer)

    #: Denotes time at which the market closes (e.g., 900 for 15:00)
    close = Column(Integer)

    description = Column(Text)


class Symbol(Base):
    """This may represents a particular company (e.g., Google, Microsoft, etc.)
    or an index (e.g., S&P 500, KOSPI 200, etc.)"""
    __tablename__ = 'symbol'

    id = Column(Integer, primary_key=True)
    market_id = Column(BigInteger, ForeignKey('market.id'))

    #: e.g., Amazon, Google, 다음카카오
    name = Column(String)

    #: e.g., AMZN, GOOG, 035720
    code = Column(String)

    market = relationship('Market', backref=backref('symbols'))


class Ticker(Base):
    __tablename__ = 'ticker'

    id = Column(Integer, primary_key=True)
    symbol_id = Column(BigInteger, ForeignKey('symbol.id'))

    symbol = relationship('Symbol', backref=backref('tickers'))

    # timestamp = Column()
    # granularity = Column() # e.g., 5 min, 1 day, 1 week, etc.
    # volume = Column()
    # open = Column()
    # close = Column()
    # low = Column()
    # high = Column()


class Article(Base):
    """Represents a news/blog article"""
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
