from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY


db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    authors = db.Column(ARRAY(db.String))
    publish_date = db.Column(db.DateTime(timezone=False))
    fetch_date = db.Column(db.DateTime(timezone=False))
    title = db.Column(db.String)
    text = db.Column(db.Text)


class Word(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    word = db.Column(db.String)
    language = db.Column(db.String(10))


article_word_assoc = db.Table(
    'article_word_assoc',
    db.Column('article_id', db.BigInteger, db.ForeignKey('article.id')),
    db.Column('word_id', db.BigInteger, db.ForeignKey('word.id'))
)


# We also need a web page fetcher and a URL extractor but we probably want to
# make them as an independent module
