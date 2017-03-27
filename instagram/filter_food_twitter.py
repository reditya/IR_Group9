import json
import sys
from collections import defaultdict
from nltk import word_tokenize, bigrams
import re
from nltk.corpus import stopwords # Import the stop word list

# 
post_file = sys.argv[1]
out_file = sys.argv[2]
food_file = sys.argv[3]

# Document to write in
outfile = open(out_file, 'w')

# Stop words list in english
stopwords_english = set(stopwords.words("english"))

english_dict = open(food_file, "r").read().split('\n')
english_size = len(english_dict) - 1

episodes = defaultdict(list)

for line in open(post_file, 'r'):
    test = json.loads(line)
    if test['lang'] == "en":
        text = test['text']
        # print text
        # remove punctuation (using regular expression)
        letters_only = re.sub("[^a-zA-Z]", " ", text)
        #print letters_only
        tokens = word_tokenize(letters_only.lower().decode('utf-8'))

        # Remove stop words in all espisodes of the corpus
        food_term = []
        tokens = [w for w in tokens if not w in stopwords_english]
        tokens_bigram = list(bigrams(tokens))
        dict_word = english_dict[0]

        # Filter one-word food term
        for w in tokens:
            dict_indix = 0
            #print w
            while dict_indix < english_size and w != english_dict[dict_indix]:
                dict_indix = dict_indix + 1
            if dict_indix != english_size and english_dict[dict_indix] not in food_term:  
                food_term.append(english_dict[dict_indix])

        # filter two-word food term
        for w in tokens_bigram:
            w = " ".join(w)
            dict_indix = 0
            #print w
            while dict_indix < english_size and w != english_dict[dict_indix]:
                dict_indix = dict_indix + 1
            if dict_indix != english_size and english_dict[dict_indix] not in food_term:	
                food_term.append(english_dict[dict_indix])

    	#print "food term: "
    	#print food_term					

        if food_term:
        	test['food'] = food_term
        	json.dump(test, outfile)
        	outfile.write('\n')		

