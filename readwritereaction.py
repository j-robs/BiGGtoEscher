import json
reactions = raw_input("enter name of file containing reaction list: ")

BiGGIDdict = {}
reactionlist = []
BiGGIDlist = []
direction = []

def createreact():
	"""Pulls reactions from specified file and deposits in a list 'reactionlist'."""
	
	with open(reactions) as freactions:
		prompt = "Enter BiGG ID for desired reaction (case sensitive!) then press enter to add the next."
		prompt += "\nTo use all BiGG IDs from dataset, type 'all' then press enter."
		prompt += "\nWhen you are done, type 'done', then press enter. "
		
		active = True
		while active:
			search = raw_input(prompt)
		#user input searches for a BiGG ID in the file to pull equation, then loops to allow multiple searches
			print(search)
		
			if search == "done":
				active = False
				#if the user types done the while loop closes
			elif search == "all":
				for line in freactions:
					if line.endswith("-") or line.endswith(">") or line.endswith("<") or line.endswith("="):
						continue
					else:
						BiGGID,equation = line.split(":")
						equation = equation.replace("\n", "")
						reactionlist.append(equation)
						BiGGIDlist.append(BiGGID)
						if "<--" in equation:
							direction.append("r")
						elif "-->" in equation:
							direction.append("f")
						elif "<=>" in equation:
							direction.append("e")
						else:
							direction.append("Unknown")
				active = False
				#if the user types all every reaction ID, equation and direction is pulled into its respective list and the while loop closes
			else:
				for line in freactions:
					if line.startswith(search + ":"):
						BiGGID,equation = line.split(":")
						equation = equation.replace("\n", "")
						reactionlist.append(equation)
						BiGGIDlist.append(BiGGID)
						if "<--" in equation:
							direction.append("r")
						elif "-->" in equation:
							direction.append("f")
						elif "<=>" in equation:
							direction.append("e")
						else:
							direction.append("Unknown")
						break
					else:
						continue
			#if the user types anything else then it is searched for in the file, line by line
			#if a line starts with the query it is pulled and the user is asked for the next input

createreact()
#print BiGGIDlist
#print reactionlist
#print direction
def makedict():
	"""Writes BiGGIDs as keys in dictionary and stores equations and directions within them"""
	for ID, eq, dr in zip(BiGGIDlist, reactionlist, direction):
		BiGGIDdict.setdefault(ID, {'Equation': eq, 'Direction': dr})
	

def writefile():
	"""Writes a json file containing dictionary 'display'"""
	
	display = raw_input("name your output file: ")
	display += ".json"
	with open(display,'w') as fdisplay:
		json.dump(BiGGIDdict, fdisplay)
		#dictionary is written to new json file
makedict()
writefile()	
