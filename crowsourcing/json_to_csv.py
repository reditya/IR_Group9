import json
import csv
from sys import argv

script, inp,inp2, out = argv
def convert_to_csv(inp_file):

	data_json = open(inp_file, mode='r').read() #reads in the JSON file into Python as a string
	data_python = json.loads(data_json) #turns the string into a json Python object
	
	for line in data_python['hits']['hits']:
		list_e = line.get('_source').get('food')
		list_n = []
		for i in list_e:
			list_n.append(i.encode('unicode_escape'))

		writer.writerow([line.get('_source').get('text').encode('unicode_escape'),list_n])


csv_out = open(out, mode='w') #opens csv file
writer = csv.writer(csv_out) #create the csv writer object
fields = ['text', 'food'] #field names
writer.writerow(fields) #writes field
convert_to_csv(inp)	
convert_to_csv(inp2)
csv_out.close()
