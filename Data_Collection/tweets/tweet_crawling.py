import tweepy
from tweepy import StreamListener
from tweepy import Stream
import json
import time

# Consumer keys and access tokens, used for OAuth.
consumer_key="qbxwtVBPewGGScwEkuQIt7ZFe"
consumer_secret="nsrBK4ZJ8zEUDB9xxLyeHsOuFgBNjqHhYo98Eg6sz7g7TJ9yzJ"
access_token="2700449264-FNgbYs2Kfqb970IGHia01lQ6larp28Fb7SdqFDj"
access_token_secret="8hrvylo0ehUAZPBQ5cBNCh9Vv1lJ6oQMV1Aji3rOgfK2j"


file = open('test_twitter_crawling_2.json', 'a')  # File in which the retrieved tweet data are stored.

# Class used to get incoming tweets.
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.start_time = time.time()
        self.time_limit = 57600 # 16 hours: 576000
        self.nbPosts = 0
        self.nbPosts_schiphol_coordinate = 0
        self.nbPosts_schiphol_name = 0
        print('start time: ' + str(self.start_time))

    def on_data(self, data):
    	if (time.time() - self.start_time) < self.time_limit :
    	    self.nbPosts = self.nbPosts + 1
            json_data = json.loads(data)
            print('Nb posts: %i' % self.nbPosts)
            json.dump(json_data,file) #Add collected data to the file.
            file.write('\n')
            return True  
        else:
            file.close()
            return False	  

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 
if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
 
    stream = Stream(auth, listener)
    filtered_tweets = stream.filter(locations=[4.73,52.29,4.98,52.42]) #Filter tweets only coming from Amsterdam.

    print('Total number of posts: %i' % listener.nbPosts)
