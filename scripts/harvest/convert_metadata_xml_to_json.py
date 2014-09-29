#!/usr/bin/python
import sys
import re
from subprocess import call
import glob
import os

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

ifile= sys.argv[1]
ofile= sys.argv[2]
ofp= open(ofile, 'a')

state= 0
lines= open(ifile)
for line in lines:

	if state == 0 and re.search('<record>', line):
		state= 1
		n_set_specs = 0
		set_specs = []
		n_authors = 0
		n_affiliations = 0
		authors = []
		affiliations = []
		affiliation = ''
		publication = ''
		title = ''
		abstract = ''
		continue

	if state == 1 and re.search('<arxiv_id>', line):
		arxiv_id= find_between(line, '<arxiv_id>', '</arxiv_id>')
		# print 'found arxiv_id = ' + arxiv_id
		continue

	if state == 1 and re.search('<n_set_specs>', line):
		n_set_specs= find_between(line, '<n_set_specs>', '</n_set_specs>')
		continue

	if state == 1 and re.search('<set_spec>', line):
		set_spec= find_between(line, '<set_spec>', '</set_spec>')
		set_specs.append(set_spec)
		continue

	if state == 1 and re.search('<created>', line):
		created= find_between(line, '<created>', '</created>')
		continue

	if state == 1 and re.search('<title>', line):
		title= find_between(line, '<title>', '</title>')
		title= title.replace('\\', '')
		title= title.replace('\'', '')
		continue

	if state == 1 and re.search('<abstract>', line):
		abstract= find_between(line, '<abstract>', '</abstract>')
		abstract= abstract.replace('\\', '')
		abstract= abstract.replace('\'', '')
		continue

	if state == 1 and re.search('<publication>', line):
		publication= find_between(line, '<publication>', '</publication>')
		publication= publication.replace('\\', '')
		publication= publication.replace('\'', '')
		continue

	if state == 1 and re.search('<n_authors>', line):
		n_authors = find_between(line, '<n_authors>', '</n_authors>')
		continue

	if state == 1 and re.search('<author>', line):
		author_found = True;
		affiliation_found = False;
		state= 2
		continue

	if state == 2 and re.search('<name>', line):
		name= find_between(line, '<name>', '</name>')
		name= name.replace('\\', '')
		name= name.replace('\'', '')
		# print 'found author with name [' + name + ']'
		authors.append(name)
		continue

	if state == 2 and re.search('<affiliation>', line):
		affiliation= find_between(line, '<affiliation>', '</affiliation>')
		affiliation= affiliation.replace('\\', '')
		affiliation= affiliation.replace('\'', '')
		affiliations.append(affiliation)
		affiliation_found = True;
		continue

	if state == 2 and re.search('</author>', line):
		state= 1
		continue

	if state == 1 and re.search('</record>', line):
		state= 0
		ofp.write('{"arxiv_id":"' + arxiv_id + '"')
		ofp.write(',"authors":[')
		n= len(authors)
		n_authors = n
		if n > 0:
			for i in range(0, n-1):
				ofp.write('"' + authors[i] + '",')
			ofp.write('"' + authors[n-1] + '"')
		ofp.write(']')
 
		ofp.write(',"set_specs":[')
		n= len(set_specs)
		if n > 0:
			for i in range(0, n-1):
				ofp.write('"' + set_specs[i] + '",')
			ofp.write('"' + set_specs[n-1] + '"')
		ofp.write(']')

		ofp.write(',"affiliations":[')
		n= len(affiliations)
		n_affiliations = n
		if n > 0:
			for i in range(0, n-1):
				ofp.write('"' + affiliations[i] + '",')
			ofp.write('"' + affiliations[n-1] + '"')
		ofp.write(']')

		if author_found == True and affiliation_found == False:
			print 'arxiv(%s) mismatch between authors(%d) and affiliations(%d)' % (arxiv_id, n_authors, n_affiliations)

		ofp.write(',"date":"' + created + '"')
		ofp.write(',"publication":"' + publication + '"')
		ofp.write(',"title":"' + title + '"')
		ofp.write(',"abstract":"' + abstract + '"')

		ofp.write('}\n')
		continue

ofp.close()
sys.exit(0)
