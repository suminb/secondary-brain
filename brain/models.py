from sqlalchemy import Column, Integer, BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Market(Base):
    __tablename__ = 'market'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    #: Represents a region to which this market belongs to (e.g., US, KR)
    region = Column(String)

    description = Column(Text)


class Symbol(Base):
    """This may represents a particular company (e.g., Google, Microsoft, etc.)
    or an index (e.g., S&P 500, KOSPI 200, etc.)"""
    __tablename__ = 'symbol'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)


class Ticker(Base):
    __tablename__ = 'ticker'

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(BigInteger)

    # timestamp = Column()
    # volume = Column()
    # open = Column()
    # close = Column()
    # low = Column()
    # high = Column()
