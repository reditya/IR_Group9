with open("food.csv") as f:
	next(f)
	for line in f: 
		content = line.split(",")
		for term in content:
			term = term.lstrip() # remove leading spaces
			term = term.replace("\"", "") # remove "
			if len(term)>1:
				print term