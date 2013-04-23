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
        print '%s already exists.' % feed_url

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

        feed.timestamp_fetched = timestamp_fetched
        db.session.commit()

if __name__ == '__main__':
    #add_feed('http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk')
    #add_feed('http://uanews.org/rss/campus-news')
    add_feed('http://feeds.foxnews.com/foxnews/health')
    fetch_feed_items()