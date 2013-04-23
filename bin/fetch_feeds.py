import sys, os
sys.path.insert(0, os.path.abspath('.'))

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

    db.session.add(feed)
    db.session.commit()


if __name__ == '__main__':
    add_feed('http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk')