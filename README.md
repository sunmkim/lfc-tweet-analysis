# Analysis of Tweets on Liverpool FC games for the 15/16 Barclays Premier League Season
The goal of this project is to collect real-time stream of tweets, and analyse & visualise that data. I will not cover all Liverpool games of the 15/16 season, only a few notable ones.

## Libraries used
- Pymongo
- Tweepy
- Pandas
- Vincent
- NLTK

## Python (~.py) files 
**streamer.py** - Creates a listener that collects tweets in real-time and stores them in a MongoDB collection.

**to_csv.py** - Creates and writes a csv file named `tweets.csv` from data stored in MongoDB

**graph.py** - Converts data in `tweets.csv` to a pandas time series and creates a graph with [Vincent](http://vincent.readthedocs.org/en/latest/).

**word_freq.py** - Filters out texts in `tweets.csv`, looking for relevant words, and plots a frequency distribution of those words using the [NLTK](http://www.nltk.org/) platform.

In the stream listener, as found in `streamer.py`, I'm specifically listening for tweets that contain the words 'liverpool', 'lfc', or 'liverpoolfc'.

## Arsenal-Liverpool Tweet Analysis (08/24/2015)
My first game of analysis was the Arsenal-Liverpool game on August 24, played at the Emirates Stadium. I started the live twitter stream right at kick-off, which was around 3:00pm EST. The stream was activated for the entirety of the game, and turned off at 4:53pm EST, a few minutes after the final whistle. Using the scripts from `graph.py` and `word_freq.py`, I had a time-series plot of the volume of tweets with relevant key words, and a frequency distribution of the most common words found in my data. First, let us examine the time-twitter volume plot.
### Twitter volume as a function of time
Here is the graph of relevant tweets as a function of time:
![Alt text](https://raw.github.com/kimasx/lfc-tweet-analysis/master/time_series.png "Twitter Volume vs Time")
Examining the data, it seems that each peak corresponds with a memorable event in the game, i.e. a goal-scoring opportunity, booking, etc. The first spike that we see in the plot, around 03:04, correspond with this exact moment, when Coutinho hits the bar:

![Alt text](http://gfycat.com/CourteousImportantFieldspaniel)



<!-- ![Alt text](https://raw.github.com/kimasx/lfc-tweet-analysis/master/word_freq.png "Word Counts") -->


