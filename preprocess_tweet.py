import json

tweets = []
for line in open('test_twitter_crawling_clean.json', 'r'):
    test = json.loads(line)
    coor = test['coordinates'][0]
    coor_1 = coor[0]
    coor_2 = coor[2]
    middle = [(coor_1[0] + coor_2[0]/2) , (coor_1[1] + coor_2[1]/2)]
    test['middle'] = middle
    tweets.append(test)

json.dump(tweets, open('test_twitter_crawling_clean.json','w'))
