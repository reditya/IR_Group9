import json
from collections import defaultdict
from nltk import word_tokenize
import re
from nltk.corpus import stopwords # Import the stop word list


# Document to write in
outfile = open('test_twitter_crawling_2_clean_filter.json', 'w')

# Stop words list in english
stopwords_english = set(stopwords.words("english"))
stopwords_dutch = set(stopwords.words("dutch"))
stopwords_french = set(stopwords.words("french"))

english_dict = open("test_english_dict.txt", "r").read().split('\n')
english_size = len(english_dict) - 1
dutch_dict = open("test_dutch_dict.txt", "r").read().split('\n')
dutch_size = len(dutch_dict) - 1
french_dict = open("test_french_dict.txt", "r").read().split('\n')
french_size = len(french_dict) - 1

episodes = defaultdict(list)

for line in open('test_twitter_crawling_2_clean.json', 'r'):
    test = json.loads(line)
    text = test['text']
    #print text
    # remove punctuation (using regular expression)
    letters_only = re.sub("[^a-zA-Z]", " ", text)
    #print letters_only
    tokens = word_tokenize(letters_only.lower().decode('utf-8'))
    
    # Remove stop words in all espisodes of the corpus
    food_term = []
    if test['lang'] == 'en':
    	tokens = [w for w in tokens if not w in stopwords_english]
    	dict_word = english_dict[0]
    	for w in tokens:
    		dict_indix = 0
    		print w
    		while dict_indix < english_size and w != english_dict[dict_indix]:
    			dict_indix = dict_indix + 1
    		if dict_indix != english_size:	
    			food_term.append(english_dict[dict_indix])
    	print "food term: "
    	print food_term					
    elif test['lang'] == 'nl':
    	tokens = [w for w in tokens if not w in stopwords_dutch]
    	dict_word = dutch_dict[0]
    	for w in tokens:
    		dict_indix = 0
    		print w
    		while dict_indix < dutch_size and w != dutch_dict[dict_indix]:
    			dict_indix = dict_indix + 1
    		if dict_indix != dutch_size:	
    			food_term.append(dutch_dict[dict_indix])
    	print "food term: "
    	print food_term
    elif test['lang'] == 'fr':
    	tokens = [w for w in tokens if not w in stopwords_french]
    	dict_word = french_dict[0]
    	for w in tokens:
    		dict_indix = 0
    		print w
    		while dict_indix < french_size and w != french_dict[dict_indix]:
    			dict_indix = dict_indix + 1
    		if dict_indix != french_size:	
    			food_term.append(french_dict[dict_indix])
    	print "food term: "
    	print food_term
    else:
    	print('Wrong Language!!!')
    if food_term:
    	test['food'] = food_term
        """
        coor = test['coordinates'][0]
        coor_1 = coor[0]
        coor_2 = coor[2]
        middle = [(coor_1[0] + coor_2[0]/2) , (coor_1[1] + coor_2[1]/2)]
        test['middle'] = middle
        """
    	json.dump(test, outfile)
    	outfile.write('\n')


		

