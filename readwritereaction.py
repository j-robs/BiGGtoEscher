import json
reactions = input("enter name of file containing reaction list: ")


def createreact():
	"""Pull components from each line of specified file and deposit in lists."""
	BIGGIDlist = []
	direction = []
	lhs1 = []
	lhs = []
	rhs1 = []
	rhs = []

	
	with open(reactions) as freactions:
		prompt = "Enter BiGG ID for desired reaction (case sensitive!) then press enter to add the next."
		prompt += "\nTo use all BiGG IDs from dataset, type 'all' then press enter."
		prompt += "\nWhen you are done, type 'done', then press enter. "
		
		active = True
		while active:
			search = input(prompt)
			#user input searches for a BiGG ID in the file to pull equation, then loops to allow multiple searches
			if search == "done":
				active = False
				#if the user types done the while loop closes
			elif search == "all":
				freactions.seek(0)
				for line in freactions:
					if line.endswith("-") or line.endswith(">") or line.endswith("<") or line.endswith("=") or line.endswith(":"):
						continue
					else:
						BIGGID,equation = line.split(":")
						equation = equation.replace("\n", "")
						BIGGIDlist.append(BIGGID)
						if "<--" in equation:
							direction.append(False)
							lefthand,righthand = equation.split("<--")
							lhs1 = [metab.strip() for metab in lefthand.split("+")]
							rhs1 = [metab.strip() for metab in righthand.split("+")]
						elif "-->" in equation:
							direction.append(False)
							lefthand,righthand = equation.split("-->")
							lhs1 = [metab.strip() for metab in lefthand.split("+")]
							rhs1 = [metab.strip() for metab in righthand.split("+")]
						elif "<=>" in equation:
							direction.append(True)
							lefthand,righthand = equation.split("<=>")
							lhs1 = [metab.strip() for metab in lefthand.split("+")]
							rhs1 = [metab.strip() for metab in righthand.split("+")]
						else:
							direction.append("Unknown")
							lhs1.append("Unknown")
							rhs1.append("Unknown")
						lhs.append(lhs1)
						rhs.append(rhs1)
						print(BIGGIDlist)
				active = False
				#if the user types all every reaction ID, equation, left hand side, right hand side 
				#and direction is pulled into its respective list and the while loop closes
			else:
				freactions.seek(0)
				for line in freactions:
					if line.startswith(search + ":"):
						BIGGID,equation = line.split(":")
						equation = equation.replace("\n", "")
						BIGGIDlist.append(BIGGID)
						if "<--" in equation:
							direction.append(False)
							lefthand,righthand = equation.split("<--")
							lhs1 = [metab.strip() for metab in lefthand.split("+")]
							rhs1 = [metab.strip() for metab in righthand.split("+")]
						elif "-->" in equation:
							direction.append(False)
							lefthand,righthand = equation.split("-->")
							lhs1 = [metab.strip() for metab in lefthand.split("+")]
							rhs1 = [metab.strip() for metab in righthand.split("+")]
						elif "<=>" in equation:
							direction.append(True)
							lefthand,righthand = equation.split("<=>")
							lhs1 = [metab.strip() for metab in lefthand.split("+")]
							rhs1 = [metab.strip() for metab in righthand.split("+")]
						else:
							direction.append("Unknown")
							lhs1 = "Unknown"
							rhs1 = "Unknown"
						lhs.append(lhs1)
						rhs.append(rhs1)
						break
					else:
						continue
				else: print("Reaction not found. Check spelling and make sure the reaction is present in your input file. ")
						
	
	#if the user types anything else then it is searched for in the file, line by line
	#if a line starts with the query it is pulled and the user is asked for the next input
	return BIGGIDlist, direction, lhs, rhs

def metabolitewriter(list, int):
	"""Create a two component dictionary for each metabolite in a list.
	
	List is a list of metabolites and int is a coefficient, either 1 or -1, defined in makedict.
	"""
	metabolites = []
	for metabolite in list:
		coefficient = int
		metabolitedict = {"coefficient":coefficient,"bigg_id":metabolite}
		metabolites.append(metabolitedict)
	return metabolites


def nodepos(int, list, counter):
	"""Define coordinates for each node on a single side of a reaction.
	
	int -- the y coordinate of the reaction
	list -- the list of metabolites
	counter -- the number of metabolites in list
	"""
	nodeposy = ((int + ((len(list) * 100) - 100)) - (200 * (counter - 1)))
	return nodeposy

def segments(markerdict, reactnodedictleft, reactnodedictright, segnumber, totalcount):
	"""Generate a dictionary for a set of segments to define node connections in Escher.
	
	markerdict -- dictionary containing a reaction ID and its unique numerical ID
	reactnodedictleft -- dictionary containing metabolite IDs and their unique numerical IDs (left side)
	reactnodedictright -- dictionary containing metabolite IDs and their unique numerical IDs (right side)
	segnumber -- a unique number assigned to each segment or join, starting from 1.
	"""
	segdict = {} 
	segdict.setdefault(1 + totalcount, {"from_node_id": str(markerdict[1 + totalcount]), "to_node_id": str(markerdict[2 + totalcount]), "b1": None, "b2": None})
	segdict.setdefault(1 + totalcount, {"from_node_id": str(markerdict[1 + totalcount]), "to_node_id": str(markerdict[3 + totalcount]), "b1": None, "b2": None})
	for key in reactnodedictleft:
		segnumber += 1
		segdict.setdefault(segnumber, {"from_node_id": str(key), "to_node_id": str(markerdict[2 + totalcount]), "b1": None, "b2": None})
	for key in reactnodedictright:
		segnumber += 1
		segdict.setdefault(segnumber, {"from_node_id": str(key), "to_node_id": str(markerdict[3 + totalcount]), "b1": None, "b2": None})
	return segdict, segnumber

def makedict(display):
	"""Writes BiGGIDs as keys in dictionary and stores equations and directions within them"""
	dictlist = [{"map_name":display,"map_id":"idnumber","map_description":display + "\nLast Modified Wed Jan 30 2019 12:10:36 GMT+0000 (Greenwich Mean Time)","homepage":"https://escher.github.io","schema":"https://escher.github.io/escher/jsonschema/1-0-0#"}]
	idnum = 1000000
	idnum2 = 1500000
	posx = 0
	posy = 0
	BIGGIDdict = {}
	reactiondict = {}
	nodedict = {}
	nodes = {}
	segnumber = 0
	totalcount = 0
	BIGGIDlist, direction, lhs, rhs = createreact()
	for ID, dr, lh, rh in zip(BIGGIDlist, direction, lhs, rhs):
		reactnodedictleft = {}
		reactnodedictright = {}
		markerdict = {}
		lhcount = 0
		rhcount = 0
		idnum += 1
		posx += 500
		posy += 500
		for metab in lh:
			idnum2 += 1
			lhcount += 1
			nodedict.setdefault(idnum2, {"node_type": "metabolite", "x": (posx - 200), "y": nodepos(posy, lh, lhcount), "bigg_id": metab, "name": "", "label_x": (posx - 200), "label_y": nodepos(posy, lh, lhcount), "node_is_primary": False})
			reactnodedictleft.setdefault(idnum2, metab)
		for metab in rh:
			idnum2 += 1
			rhcount +=1
			nodedict.setdefault(idnum2, {"node_type": "metabolite", "x": (posx + 200), "y": nodepos(posy, rh, rhcount), "bigg_id": metab, "name": "", "label_x": (posx + 200), "label_y": nodepos(posy, rh, rhcount), "node_is_primary": False})
			reactnodedictright.setdefault(idnum2, metab)
		idnum2 += 1
		nodedict.setdefault(idnum2, {"node_type": "midmarker", "x": posx, "y": posy})
		segnumber += 1
		markerdict.setdefault(segnumber, idnum2)
		idnum2 += 1
		nodedict.setdefault(idnum2, {"node_type": "multimarker", "x": (posx - 20), "y": posy})
		segnumber += 1
		markerdict.setdefault(segnumber, idnum2)
		idnum2 += 1
		nodedict.setdefault(idnum2, {"node_type": "multimarker", "x": (posx + 20), "y": posy})
		segnumber += 1
		markerdict.setdefault(segnumber, idnum2)
		segdict, segnumber = segments(markerdict, reactnodedictleft, reactnodedictright, segnumber, totalcount)
		reactiondict.setdefault(idnum,{"name":"","bigg_id":ID,"reversibility":dr,"label_x":posx,"label_y":posy,"gene_reaction_rule":"","genes":[],"metabolites":metabolitewriter(lh, -1)+metabolitewriter(rh, 1),"segments": segdict})
		totalcount += 3
		totalcount += lhcount
		totalcount += rhcount
		
		BIGGIDdict.setdefault("reactions", reactiondict)
		BIGGIDdict.setdefault("nodes", nodedict)
	
	posx += 500
	posy += 500
	BIGGIDdict.setdefault("text_labels", {})
	BIGGIDdict.setdefault("canvas", {"x":0,"y":0,"width":posx,"height":posy})
	dictlist.append(BIGGIDdict)
	return dictlist
	
def writefile():
	"""Writes a json file containing dictionary 'display'"""
	display = input("name your output file: ")
	display2 = display + ".json"
	with open(display2,'w') as fdisplay:
		json.dump(makedict(display), fdisplay)
		#dictionary is written to new json file


writefile()	
	
