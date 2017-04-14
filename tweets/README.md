# Purpose
This folder contains all the files used to crawl Twitter and preprocess the tweets.

# File description
- **twitter_crawling.py**: python script to crawl Twitter within Amsterdam.
- **filter_1_tweet.py**: first script used to preprocess the posts: filter tweets per coordinate and language.
- **filter_2_tweet_food.py**: second script used to preprocess the posts: filter tweets per food terms.
- **filter_3_tweet_sentiment.py**: filter tweets per sentiment.
- **twitter_food.json**: file resulting from the crawling and preprocessing steps.
- **elasticcommands**, **script/**: contains script to index the data into ElasticSearch.
