import pandas as p
import vincent
from pandas.tseries.resample import TimeGrouper
from pandas.tseries.offsets import DateOffset

tweets = p.read_csv('./tweets.csv')

tweets['created_at'] = p.to_datetime(p.Series(tweets['created_at']))

# set index to 'created_at'
tweets.set_index('created_at', drop=False, inplace=True)
tweets.index = tweets.index.tz_localize('GMT').tz_convert('EST')

# convert to 12 hour format
tweets.index = tweets.index - DateOffset(hours = 12)

# created_at index is formatted to per minute
tweets_pm = tweets['created_at'].resample('1t', how='count')

# create time series graph via Vincent
vincent.core.initialize_notebook()
area = vincent.Area(tweets_pm)
area.colors(brew='Spectral')
area.display()