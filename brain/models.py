# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, \
    Float, Enum
from sqlalchemy import ForeignKey, UniqueConstraint
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

    currency = Column(String)

    description = Column(Text)


class Symbol(Base):
    """This may represents a particular company (e.g., Google, Microsoft, etc.)
    or an index (e.g., S&P 500, KOSPI 200, etc.)"""
    __tablename__ = 'symbol'
    __table_args__ = (UniqueConstraint('market_id', 'symbol', name='unique_symbol'),)

    id = Column(Integer, primary_key=True)
    market_id = Column(BigInteger, ForeignKey('market.id'))

    #: e.g., Amazon, Google, 다음카카오
    name = Column(String)

    #: e.g., AMZN, GOOG, 035720
    symbol = Column(String)

    market = relationship('Market', backref=backref('symbols'))


class Ticker(Base):
    __tablename__ = 'ticker'

    id = Column(Integer, primary_key=True)
    symbol_id = Column(BigInteger, ForeignKey('symbol.id'))

    symbol = relationship('Symbol', backref=backref('tickers'))

    timestamp = Column(DateTime)
    granularity = Column(Enum('1sec', '1min', '5min', '1hour', '1week', '1month'))
    volume = Column(Integer)
    # The purpose of this project is not to create an accounting software
    # providing 100% precision, but it is rather a statistical tool providing
    # reasonable performance and adequate precision. Hence the use of
    # floating point type is an acceptable compromise.
    open = Column(Float(precision=64))
    close = Column(Float(precision=64))
    low = Column(Float(precision=64))
    high = Column(Float(precision=64))


class Article(Base):
    """Represents a news/blog article"""
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
