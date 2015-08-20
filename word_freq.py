import nltk, pandas

from nltk.corpus import stopwords
from nltk import FreqDist

stop = stopwords.words('english')
texts = pandas.read_csv('./tweets.csv')['text']

tokens = []

for text in texts.values:
  tokens.extend([word.lower().strip(':,.-') for word in text.split()])

filtered_tokens = [word for word in tokens if not word in stop]

freq_dist = nltk.FreqDist(filtered_tokens)
freq_dist.plot(20)