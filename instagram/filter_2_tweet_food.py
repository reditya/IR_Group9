import json
from collections import defaultdict
from nltk import word_tokenize
import re
from nltk.corpus import stopwords # Import the stop word list


# Document to write in
outfile = open('output.txt', 'w')

# Stop words list in english
stopwords_english = set(stopwords.words("english"))

english_dict = open("food_term.txt", "r").read().split('\n')
english_size = len(english_dict) - 1

episodes = defaultdict(list)

for line in open('instagram_amsterdamfood.txt', 'r'):
    test = json.loads(line)
    text = test['text']
    #print text
    # remove punctuation (using regular expression)
    letters_only = re.sub("[^a-zA-Z]", " ", text)
    #print letters_only
    tokens = word_tokenize(letters_only.lower().decode('utf-8'))
    
    # Remove stop words in all espisodes of the corpus
    food_term = []
    tokens = [w for w in tokens if not w in stopwords_english]
    dict_word = english_dict[0]
    for w in tokens:
        dict_indix = 0
        #print w
        while dict_indix < english_size and w != english_dict[dict_indix]:
            dict_indix = dict_indix + 1
        if dict_indix != english_size:	
            food_term.append(english_dict[dict_indix])

	#print "food term: "
	#print food_term					

    if food_term:
    	test['food'] = food_term
    	json.dump(test, outfile)
    	outfile.write('\n')		

