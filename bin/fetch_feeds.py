import sys, os
sys.path.insert(0, os.path.abspath('.'))

from sqlalchemy.exc import IntegrityError
from app.core import db
from app.models import *

import uuid
import datetime

import feedparser

def __tmp__():

    feed = Feed(id=str(uuid.uuid4()), timestamp_fetched=datetime.datetime.now(), feed_url='http://localhost')

    db.session.add(feed)
    db.session.commit()


def add_feed(feed_url):
    # TODO: verify feed_url is in a valid format

    print 'Adding a new feed: %s' % feed_url

    feed_url = feed_url.strip()

    fp = feedparser.parse(feed_url)

    feed = Feed(
        id=str(uuid.uuid4()),
        feed_url=feed_url,
        web_url=fp['url'],
        version=fp['version'],
        title=fp['channel']['title'],
        description=fp['channel']['description'],
    )

    try:
        db.session.add(feed)
        db.session.commit()

    except IntegrityError as e:
        print 'Feed already exists: %s' % feed_url
        db.session.rollback()

def fetch_feed_items():
    """Parses a set of feeds and insert feed items into the database."""

    for feed in Feed.query.filter(or_(
            Feed.timestamp_fetched == None,
            Feed.timestamp_fetched <= datetime.datetime.now() - datetime.timedelta(hours=1))
        ).all():

        fp = feedparser.parse(feed.feed_url)
        timestamp_fetched = datetime.datetime.now()

        for item in fp['items']:

            print 'Processing "%s"' % item['link']

            feed_item = FeedItem.query.filter_by(link=item['link']).first()

            if feed_item != None:
                print '%s already exists.' % feed_item.link

            else:
                feed_item = FeedItem(
                    id=str(uuid.uuid4()),
                    feed_id=feed.id,
                    timestamp_published=item['published'],
                    timestamp_fetched=timestamp_fetched,
                    title=item['title'],
                    link=item['link'],
                    description=item['summary'],
                )

                db.session.add(feed_item)
                db.session.commit()

        feed.timestamp_fetched = timestamp_fetched
        db.session.commit()

def build_word_index():
    from bs4 import BeautifulSoup

    for feed_item in FeedItem.query.filter(
            FeedItem.timestamp_fetched >= datetime.datetime.now() - datetime.timedelta(minutes=3)
        ).all():

        text = feed_item.description

        soup = BeautifulSoup(text)

        # TODO: This is not sufficient
        words = map(lambda w: w.lower(), soup.get_text().split())

        print 'Indexing: %s' % words

        for word in set(words):
            word_index = WordIndex.query.get((word, feed_item.id))

            if word_index != None:
                print 'Already exists: %s : %s' % (word, feed_item.id)

            else:
                word_index = WordIndex(word=word, entry='feed_item', entry_id=feed_item.id)

                db.session.add(word_index)

        db.session.commit()

if __name__ == '__main__':
    #add_feed('http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk')
    #add_feed('http://uanews.org/rss/campus-news')
    add_feed('http://finance.yahoo.com/insurance/?format=rss')
    fetch_feed_items()
    #build_word_index()