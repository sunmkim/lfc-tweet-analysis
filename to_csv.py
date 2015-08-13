from pymongo import MongoClient
from operator import itemgetter
import csv

db = MongoClient().lfc

with open('tweets.csv', 'w') as outfile:
  fieldnames = ['text', 'user', 'created_at', 'geo']
  writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fieldnames)
  writer.writeheader()

  for data in db.Tweets.find():
    writer.writerow({ 
      'text': data['text'].encode('utf-8'), 
      'user': data['user'].encode('utf-8'), 
      'created_at': data['created_at'],
      'geo': data['geo']
    })

  outfile.close()