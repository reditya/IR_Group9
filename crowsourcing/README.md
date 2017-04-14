## Purpose
This folder contains the evaluation via crowdsourcing of the data preprocessing step: evaluation of the sentiment analysis, food term extraction, and food-related posts recognition.

## Files explanation
- **job_1004610.json**: data extracted from Crowdflower.
- **crowdfile.csv**: data transformed from json to csv.
- **json_to_csv.py**: python script to transform the crowdflower data into an organized csv file.
- **evaluation.py**: python script to analyse the human computation results. Return percentages of correct answers, percentages of agreement, and histogram plot of forgotten words.
