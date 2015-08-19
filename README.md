# Analysis of Tweets on Liverpool FC games for the 15/16 Barclays Premier League Season
The goal of this project is to collect real-time stream of tweets, and analyse & visualise that data. I will not cover all Liverpool games of the 15/16 season, only a few notable ones.

## Libraries used
- Pymongo
- Tweepy
- Pandas
- Vincent

## Python (~.py) files 
**streamer.py** - Creates a listener that collects tweets in real-time and stores them in a MongoDB collection.

**to_csv.py** - Creates and writes a csv file named `tweets.csv` from data stored in MongoDB

**graph.py** - Converts data in `tweets.csv` to a pandas time series and creates a graph with [Vincent](http://vincent.readthedocs.org/en/latest/).