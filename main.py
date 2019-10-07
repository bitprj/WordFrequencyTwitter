import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re
import networkx

import warnings


def remove_url(txt):
    """Replace URLs found in a text string with nothing
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def main():
    warnings.filterwarnings("ignore")

    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")

    # input your credentials here
    consumer_key = 'xxx'
    consumer_secret = 'xxx'
    access_token = 'xxx'
    access_token_secret = 'xxx'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    search_term = "#twitter+api -filter:retweets"

    tweets = tw.Cursor(api.search,
                       q=search_term,
                       lang="en",
                       since='2018-11-01').items(1000)

    all_tweets = [tweet.text for tweet in tweets]

    print(all_tweets[:5])
    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
    print(all_tweets_no_urls[:5])

    # Split the words from one tweet into unique elements
    print(all_tweets_no_urls[0].split())

    # Split the words from one tweet into unique elements
    print(all_tweets_no_urls[0].lower().split())

    # Create a list of lists containing lowercase words for each tweet
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]
    print(words_in_tweet[:2])

    # List of all words across tweets
    all_words_no_urls = list(itertools.chain(*words_in_tweet))

    # Create counter
    counts_no_urls = collections.Counter(all_words_no_urls)

    print(counts_no_urls.most_common(15))

    clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
                                        columns=['words', 'count'])

    print(clean_tweets_no_urls.head())

    fig, ax = plt.subplots(figsize=(8, 8))
    # Plot horizontal bar graph
    clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
                                                           y='count',
                                                           ax=ax,
                                                           color="purple")

    ax.set_title("Common Words Found in Tweets (Including All Words)")

    plt.show()

main()
