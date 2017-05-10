# Python file to parse the list
# Now start to process the list
with open("unformat_list.txt") as f:
	# Loop through each line
	for line in f:
		# Remove white space at the end
		line = line.strip()
		# If the string is not empty
		if line:
			print line
