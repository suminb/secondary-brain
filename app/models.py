
#
# Partially copied from http://stackoverflow.com/questions/6290162/how-to-automatically-reflect-database-to-sqlalchemy-declarative
#

from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from datetime import datetime
from sqlalchemy.orm import contains_eager, joinedload
from sqlalchemy.orm import relationship

from core import db

import json

Base = declarative_base()
metadata = MetaData(db.engine)

class AlchemyEncoder(json.JSONEncoder):
    """http://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json"""

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

def serialize(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                json.dumps(data) # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields


class Feed(Base, db.Model):
    __table__ = Table('feed', metadata, autoload=True)

class FeedItem(Base, db.Model):
    __table__ = Table('feed_item', metadata, autoload=True)

class WordIndex(Base, db.Model):
    __table__ = Table('word_index', metadata, autoload=True)