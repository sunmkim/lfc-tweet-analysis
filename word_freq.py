import nltk, pandas

from nltk.corpus import stopwords
from nltk import FreqDist

# get english stopwords
stop = stopwords.words('english')
texts = pandas.read_csv('./tweets.csv')['text']

tokens = []

for text in texts.values:
  tokens.extend([word.lower().strip(':,."-') for word in text.split()])

filtered_tokens = [word.decode('utf-8') for word in tokens if not word.decode('utf-8') in stop]

freq_dist = nltk.FreqDist(filtered_tokens)
print freq_dist.plot(25)