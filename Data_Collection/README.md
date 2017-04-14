# Crawling Process

The crawling process are done for three main sources : 
1. Social media posts : Twitter and Instagram
2. Recipes : Allrecipes
3. Restaurants : Foursquare and Thuisbezorgd
3. Dictionary : Oxford Dictionary and DBPedia

## Social Media Posts
### Instagram
We use library called php-instagram-scraper to mine Instagram data. This library needs to be installed before starting the crawling process.

```
git clone https://github.com/postaddictme/instagram-php-scraper.git
```

The code ```tag.php``` is responsible for the crawling. Using this function, we can mine Instagram posts with a specific hashtag given in the first argument of the script. For our usecase, we only mined #AmsterdamFood hashtag.  

```
mkdir tag 
php tag.php amsterdamfood
```

By default, the output of the script will be saved in the directory ```tag/```. The next thing that we do is to preprocess the data and only use posts which contain location information.

```
python parse_location.py tag/amsterdamfood_result.txt getLocationPost > tag/location_amsterdamfood.txt
python parse_location.py tag/amsterdamfood_result.txt getLocationId > tag/location_id.txt
```

Once we obtain the location ID of each posts, we need to crawl the coordinate by calling ```getLocationCoordinate.py```.

```
python getLocationCoordinate.py > tag/location_coordinate.txt
```

Once we get the location coordinate, we need to combine the instagram posts with the coordinate reference.

```
python parse_json.py tag/location_amsterdamfood.txt tag/location_coordinate.txt tag/instagram_amsterdamfood.txt
```

Once we have the complete data with coordinate, we run the final preprocessing to complement the data with the foodterm that we use.

```
python filter_food_instagram.py instagram_amsterdamfood.txt instagram_food.json clean_dictio.txt
```

The ```instagram_food.json``` is the final dataset that will be indexed to the Elasticsearch instances.

### Twitter
The following file and script is responsible to produce the final dataset for tweets : 
1. ```tweet_crawling.py``` : streaming tweets in the boundary of Amsterdam. 
2. ```filter_1_tweet.py``` : remove the tweets which don't have location and also remove special characters such as @,#
3. ```filter_food_twitter.py``` : preprocess the tweets further to extract relevant tweets which contain the food term
4. ```filter_3_tweet_sentiment.py``` : responsible to preprocess the sentiment in the tweets

The final dataset that we use to be indexed in the Elasticsearch is : ```twitter_food.json```

## Allrecipes
The following file and script is responsible to produce the final dataset used for allrecipes data : 
1. ```crawler.py``` : to crawl recipes in the Dutch-version of the website
2. ```crawler_en.py``` : to crawl recipes in the English-version of the website

The final dataset is ```bitnami_new_dutch_recipes.csv``` and ```bitnami_new_english_recipes.csv```. Both of these files will be indexed to the Elasticsearch

## Thuisbezorgd
The following file and script is responsible to produce the final dataset used for the Thuisbezorgd data : 
1. ```thuisbezorgd_crawler.py``` : to crawl the thuisbezorgd website

The final dataset is ```thuisbezorgd.json```. Both of these files will be indexed to the Elasticsearch

## Dictionary
We download DBPedia metadata files and filter the term with the Food ontology. We also combine this data with the Oxford dictionary. In the end, our final dictionary is listed in ```clean_dictio.txt```.
