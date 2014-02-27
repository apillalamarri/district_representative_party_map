# district_rep_party_map.py
# Creates a map of the US with Congressional districts shaded according 
# to the party affiliation of the distric's member of Congress.
# Democrats get blue, Republicans get red, and Independents get white
# Creating using the tutorial here: http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools/
# With Congressional districts as the geography. svg file for map is here:
# http://commons.wikimedia.org/wiki/File:113th_U.S._Congress_House_districts_blank.svg
# Data on members of Congress is from The Sunlight foundation here: http://unitedstates.sunlightfoundation.com/legislators/legislators.csv
# Uses BeautifulSoup from http://www.crummy.com/software/BeautifulSoup/

import csv
# get BeautifulSoup
from bs4 import BeautifulSoup

# read in party and district data from legislators.csv
party = {}
reader = csv.reader(open('legislators.csv'), delimiter=",")
for row in reader:
	try:
		# concatenate the State value and district value, with a "-" in the middle, forming the districtCode
		# first, handle the At-Large district codes, which are written as MT-AL 
		# (for Montana At-Large) in 113th_U.S._Congress_House_districts_blank.svg
		if row[8]=='00': 
			districtCode = row[7] + "-AL"
		else:
			districtCode = row[7] + "-" + row[8]
		# print "districtCode = {0}".format(districtCode)
		# store the party affiliation of the Representative
		repParty = row [6]
		# add an entry to the party dictionary, consisting of districtCode: repParty
		party[districtCode] = repParty
	except:
		pass
		
# Load the SVG map
svg = open('113th_U.S._Congress_House_districts_blank.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# Find Congressional districts
paths = soup.findAll('path')

# Map colors: blue, red, and white for Democrats, Republicans, and Independants
colors = ["#0000FF","#FF0000","#FFFFFF"]

# District style - make the district boundaries white, along with some hand-waving that I don't understand yet
path_style='font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.3;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# Assign a color to each Congressional district based on the party affiliation of its Representative
for p in paths:
	if p['id'] not in ["State_Lines", "separator"]:
		try:
			districtRepParty = party[p['id']]
		except:
			continue
		# Democratic districts get the first color in the colors list, which is #0000FF for blue
		if districtRepParty == 'D':
			color_class = 0
		# Republican districts get the second color in the colors list, which is #FF0000 for red
		elif districtRepParty == 'R':
			color_class = 1
		# Independent districts get the third color in the colors list, which is #FFFFFF for white
		else:
			color_class = 2			
		color = colors[color_class]
		p['style'] = path_style + color

# Output map
print soup.prettify()