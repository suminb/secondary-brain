# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, \
    Float, Enum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CRUDMixin(object):
    """Copied from https://realpython.com/blog/python/python-web-applications-with-flask-part-ii/
    """  # noqa

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, session, commit: bool=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(session, commit=commit)

    @classmethod
    def get(cls, id: int):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id: int):
        return cls.query.get_or_404(id)

    def update(self, commit: bool=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, session, commit: bool=True):
        session.add(self)
        if commit:
            session.commit()
        return self

    def delete(self, session, commit: bool=True):
        session.delete(self)
        return commit and session.commit()


class Market(Base, CRUDMixin):
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


class Symbol(Base, CRUDMixin):
    """This may represents a particular company (e.g., Google, Microsoft, etc.)
    or an index (e.g., S&P 500, KOSPI 200, etc.)"""
    __tablename__ = 'symbol'
    __table_args__ = (UniqueConstraint('market_id', 'symbol',
                                       name='unique_symbol'),)

    id = Column(Integer, primary_key=True)
    market_id = Column(BigInteger, ForeignKey('market.id'))

    #: e.g., Amazon, Google, 다음카카오
    name = Column(String)

    #: e.g., AMZN, GOOG, 035720
    symbol = Column(String)

    currency = Column(String)
    instrument_type = Column(String)  # TODO: Make this enum

    market = relationship('Market', backref=backref('symbols'))


class Ticker(Base, CRUDMixin):
    __tablename__ = 'ticker'
    __table_args__ = (UniqueConstraint('symbol_id', 'timestamp', 'granularity',
                                       name='unique_ticker'),)

    id = Column(Integer, primary_key=True)
    symbol_id = Column(BigInteger, ForeignKey('symbol.id'))

    symbol = relationship('Symbol', backref=backref('tickers'))

    timestamp = Column(Integer)
    granularity = Column(Enum('1sec', '1min', '5min', '1hour', '1week',
                              '1month', name='granularity'))
    volume = Column(Integer)
    # The purpose of this project is not to create an accounting software
    # providing 100% precision, but it is rather a statistical tool providing
    # reasonable performance and adequate precision. Hence the use of
    # floating point type is an acceptable compromise.
    open = Column(Float(precision=64))
    close = Column(Float(precision=64))
    low = Column(Float(precision=64))
    high = Column(Float(precision=64))


class Article(Base, CRUDMixin):
    """Represents a news/blog article"""
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
