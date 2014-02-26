# district_rep_party_map.py
import csv
# get BeautifulSoup at http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup

#read in party and district data from legislators.csv, obtained from
#http://unitedstates.sunlightfoundation.com/legislators/legislators.csv

party = {}
reader = csv.reader(open('legislators.csv'), delimiter=",")
for row in reader:
	try:
		if row[8]=='00':
			districtCode = row[7] + "-AL"
		else:
			districtCode = row[7] + "-" + row[8]
		#print "districtCode = {0}".format(districtCode)
		RepParty = row [6]
		party[districtCode] = RepParty
	except:
		pass
		
# Load the SVG map
svg = open('113th_U.S._Congress_House_districts_blank.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# Find Congressional districts
paths = soup.findAll('path')

#Map colors
colors = ["#0000FF","#FF0000","#FFFFFF"]

# District style
path_style='font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.3;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# Color the Congressional districts based on the party affiliations of their Representatives
for p in paths:
	if p['id'] not in ["State_Lines", "separator"]:
		# pass
		try:
			districtRepParty = party[p['id']]
		except:
			continue
			
		if districtRepParty == 'D':
			color_class = 0
		elif districtRepParty == 'R':
			color_class = 1
		else:
			color_class = 2
			
		color = colors[color_class]
		p['style'] = path_style + color

# Output map
print soup.prettify()