#!/bin/sh

# Preprocessing of the tweets
# We clean the tweet text, deleting URL
# We find the language and delete tweets which are not in english or dutch
# We compute the sentiment of the remaining tweets
# We save all important tweets info in a new file
new_file=`basename $1 .json`"_clean.json"
ENG="en"
FR="fr"
NL="nl"
relevant_tweet=false;
while IFS='' read -r line || [[ -n "$line" ]]; do
    TWEET="$(echo "$line" | sed ':a;N;$!ba;s/\n/ /g' | sed 's/\"quoted_status\": {.*//'  |  sed -e 's/.*e, \"text\": \"\(.*\)\", \"is_quote.*/\1/' | sed 's/\\u.*//' | sed -e 's!http\(s\)\{0,1\}://[^[:space:]]*!!g')" #  >> sentiment_tweet.json # curl -d "text=@-" http://text-processing.com/api/sentiment/  
    LANG="$(echo "$line" | sed ':a;N;$!ba;s/\n/ /g' | sed -e 's/.*, \"lang\": \"\(.*\)\", \"created_at\".*/\1/')" 
    #if [ "$LANG" != "$ENG" ] && [ "$LANG" != "$FR" ] && [ "$LANG" != "$NL" ];
    
    location="$(echo "$line" | sed ':a;N;$!ba;s/\n/ /g' | sed -e 's/.*\"Polygon\", \"coordinates\": \(.*\)}, \"country_code\".*/\1/')";
    # First, check whether we have access to the location of the tweet
    if [ "$location" != null ];
        then
        if [ ${#LANG} != 2 ]
            then LANG="$(echo "$line" | sed ':a;N;$!ba;s/\n/ /g' | sed 's/.\", \"lang\":.*\, \"profile_background_tile\"//' | sed -e 's/.*, \"lang\": \"\(.*\)\", \"extended_tweet\".*/\1/')" ;
        fi
        #echo "$LANG" >> test.txt
        if [ "$LANG" = "$ENG" ];
    	   then relevant_tweet=true;
	    fi
	    if [ "$LANG" = "$FR" ];
    	   then relevant_tweet=true;
	    fi
	    if [ "$LANG" = "$NL" ];
    	   then relevant_tweet=true;
	    fi

	    if [ "$relevant_tweet" = true ]; 
		   then date="$(echo "$line" | sed ':a;N;$!ba;s/\n/ /g' |  sed 's/.\"created_at\":.*\, \"contributors_enabled\"//' | sed -e 's/.*\"created_at\": \"\(.*\)\", \"quoted_status_id_str\".*/\1/')";
		   if [ ${#date} != 30 ];
		      then date="$(echo "$line" | sed ':a;N;$!ba;s/\n/ /g' |  sed 's/.\"created_at\":.*\, \"contributors_enabled\"//' | sed -e 's/.*\"created_at\": \"\(.*\)\", \"filter_level\".*/\1/')";
		   fi
		   echo "{\"text\": \"${TWEET}\", \"lang\": \"$LANG\", \"coordinates\": ${location}, \"created_at\": \"$date\"}" >> $new_file  ;
		   relevant_tweet=false;
	    fi
    fi

done < "$1"
