'''
Collect real-time stream of tweets and store them in a MongoDB collection.

'''


import sys
import pymongo
import tweepy

from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener

client = pymongo.MongoClient('localhost', 27017)
db = client.test

consumer_key="1HGHBB0r4TD6wbPin2osFvABb"
consumer_secret="0fSH0pOa1X4VzJoCgKZLdwqoQuzCPJZh7eS9AJvwfYxi89htSV"

access_token="2881128166-fqcHYt7DcwGnMTyeQgAuhnKyub0OvTw7oQiwFDy"
access_token_secret="P2VCectHrHOGo9hi5fZrl8ZytBdPz2VbmzK3q22GMJNQB"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

class CustomListener(StreamListener):
  def __init__(self, api):
    self.api = api
    super(tweepy.StreamListener, self).__init__()
    self.db = pymongo.MongoClient().lfc

  def on_status(self, tweet):
    data = {}
    data['text'] = tweet.text
    data['user'] = tweet.user.screen_name
    data['created_at'] = tweet.created_at
    data['geo'] = tweet.geo
    
    print data, '\n'
    # self.db.Tweets.insert(data)

  def on_error(self, status):
    print >> sys.stderr, 'Error: ', status
    return True

  def on_timeout(self):
    print >> sys.stderr, 'Stream timeout'
    return True

listen = Stream(auth, CustomListener(api))
listen.filter(track=['liverpool'])
