# Analysis of Liverpool FC Tweets in the 15/16 Barclays Premier League Season
The goal of this project is to collect real-time stream of tweets, and analyse & visualise that data. I will not cover all Liverpool games of the 15/16 season, only a few notable ones.

## Libraries used
- Pymongo
- Tweepy
- Pandas
- Vincent
- NLTK
- Folium

## Python (~.py) files 
**streamer.py** - Creates a listener that collects tweets in real-time and stores them in a MongoDB collection.

**to_csv.py** - Creates and writes a csv file named `tweets.csv` from data stored in MongoDB.

**graph.py** - Converts data in `tweets.csv` to a pandas time series and creates a graph with [Vincent](http://vincent.readthedocs.org/en/latest/).

**word_freq.py** - Filters out texts in `tweets.csv`, looking for relevant words, and plots a frequency distribution of those words using the [NLTK](http://www.nltk.org/) platform.

**map.py** - Creates a map of geo-tagged tweets with [Folium](https://github.com/python-visualization/folium).

In the stream listener, as found in `streamer.py`, I'm specifically listening for tweets that contain the words 'liverpool', 'lfc', or 'liverpoolfc'.

## Arsenal-Liverpool Tweet Analysis (08/24/2015)
My first game of analysis was the Arsenal-Liverpool game on August 24, played at the Emirates Stadium. The game ended in a goalless draw at 0-0. I started the live twitter stream right at kick-off, which was around 3:00pm EST. The stream was activated for the entirety of the game, and turned off at 4:53pm EST, a few minutes after the final whistle. Overall, around 152,000 tweets were collected during the Arsenal-Liverpool match. Using the scripts from `graph.py` and `word_freq.py`, I had a time-series plot of the volume of tweets per minute with relevant key words, and a frequency distribution of the most common words found in my data. First, let us examine the time-twitter volume plot.

### Twitter volume per minute as a function of time
Here is the graph of relevant tweets as a function of time:
![Alt text](https://raw.github.com/kimasx/lfc-tweet-analysis/master/assets/time_series.png "Twitter Volume per Minute vs Time")
Examining the data, it seems that each peak corresponds with a memorable event in the game, i.e. a goal-scoring opportunity, booking, etc. For example. the first spike that we see in the plot, around 03:04, correspond with this exact moment, when Coutinho hits the bar:
<br>
<img src="/assets/coutinho.gif" style="display:block;">
<br>
We also see a large peak coming in at around 3:45, at almost 3,000 tweets per minute. Looking at the data, many of the tweets are about another Coutinho attempt at goal hitting the post:
<br>
<img src="/assets/bar.gif" style="display:block;">
<br>
However, we see that this peak doesn't sharply decline, but declines gradually. This is most likely due to the fact that the goal-attempt came right before half-time, allowing users to comment on their thoughts about the first half of the game for about 15 minutes before the game started again.

### Frequency distribution of 25 most common words
![Alt text](https://raw.github.com/kimasx/lfc-tweet-analysis/master/assets/word_freq.png "Word Counts")
Given the filter words, we expect `liverpool` and `#lfc` to be the most common words, so this is not surprising. We see, however, that `rt`, or retweets, is the third most frequently used word during the game. This indicates that many users were simply retweeting others' comments. The players that were most tweeted about are Cech and Coutinho. This also makes sense given each player's contribution to their respective teams and their highlight-worthy moments.

## Code Overview
Let us now examine in detail the four python files mentioned.
### streamer.py
This file uses Pymongo and Tweepy to collect real-time twitter data and store them in a MongoDB collection. The key method in the `CustomListener` class is `on_status()`:
```python
  def on_status(self, tweet):
    data = {}
    data['text'] = tweet.text
    data['user'] = tweet.user.screen_name
    data['created_at'] = tweet.created_at
    data['geo'] = tweet.geo
    
    print data, '\n'
    self.db.Tweets.insert(data)
```
On every new tweet that comes through the filtered stream, we're creating a dictionary, called `data`, with 4 keys (`text`, `user`, `created_at` and `geo`). `text` is the actual content of the tweet itself; `user` is the twitter handle of the user who posted the said tweet; `created_at` is the time when the tweet was posted; and `geo` is the location at which the tweet was created. The `geo` is only available for those users that enable geo-tracking, and thus, majority of the tweets do not have this information. Once we create the dictionary, we can store it into a MongoDB collection, called Tweets, with `self.db.Tweets.insert(data)`. Finally, we create an instance of the stream and filter for search words using an array:
```python
  listen = Stream(auth, CustomListener(api))
  listen.filter(track=['liverpool','lfc','liverpoolfc'])
```

### to_csv.py
`to_csv.py` simply writes data to a csv file using the data that we have stored in MongoDB. Using the `csv` python module, we create a writer which writes to a csv file called `tweets.csv`:
```python
with open('tweets.csv', 'w') as outfile:
  fieldnames = ['text', 'user', 'created_at', 'geo']
  writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fieldnames)
  writer.writeheader()
```
Next, we sort through the Tweets collection and write the appropriate data matching their fieldnames:
```python
for data in db.Tweets.find():
  writer.writerow({ 
    'text': data['text'].encode('utf-8'), 
    'user': data['user'].encode('utf-8'), 
    'created_at': data['created_at'],
    'geo': data['geo']
  })
```
For `text` and `user` data, we must make sure to encode any unicode to UTF-8 so that data is readable both to humans and the machine.

### graph.py
Now that we have exported our data to a csv file, we can start to analyze them by charting a plot of tweet volume over time using pandas and vincent, a library that allows us to build Vega visualizations with python. First we create a pandas dataframe, then use the `created_at` column as index to create a pandas time series.
```python
tweets = p.read_csv('./tweets.csv')
tweets['created_at'] = p.to_datetime(p.Series(tweets['created_at']))
tweets.set_index('created_at', drop=False, inplace=True)
```
We are then able to convert the data into "per minute" unit. In other words, we now have tweets per minute on the y-axis. And now we can display the plot using the color of our choice with the vincent library.
```python
# created_at index is formatted to per minute
tweets_pm = tweets['created_at'].resample('1t', how='count')

# create time series graph via Vincent
vincent.core.initialize_notebook()
area = vincent.Area(tweets_pm)
area.colors(brew='Spectral')
area.display()
```

### word_freq.py
We can also find the most commonly-used words during the Arsenal-Liverpool game with pandas and nltk. Nltk makes it very easy to process text, and probably saved me from writing a bunch more code in `word_freq.py`. To parse and proess twitter texts, we first filter out for stop words, which are high-frequency words that are often irrelevant, such as articles, prepositions, etc (think "to", "the", "also"). Then, we strip all the words in twitter texts of punctuation marks. This is so that words like "Arsenal" and "Arsenal." are not counted as two different words.
```python
# get english stopwords
stop = stopwords.words('english')
texts = pandas.read_csv('./tweets.csv')['text']

tokens = []

# strip words of punctuation marks
for text in texts.values:
  tokens.extend([word.lower().strip(':,."-') for word in text.split()])
```
Now, we create a new filtered words list after removing stop words and removing punctuation marks. Again, we have to take account Unicode encoding to make it machine readable.
```python
filtered_tokens = [word.decode('utf-8') for word in tokens if not word.decode('utf-8') in stop]
```
With help from nltk, we can easily plot a frequency distribution of the top 25 words used during the game.
```python
freq_dist = nltk.FreqDist(filtered_tokens)
print freq_dist.plot(25)
```
