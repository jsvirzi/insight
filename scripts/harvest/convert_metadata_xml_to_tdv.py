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
		n_set_specs= 0
		set_specs= []
		n_authors= 0
		authors= []
		affiliations= []
		affiliation= ''
		continue

	if state == 1 and re.search('<arxiv_id>', line):
		arxiv_id= find_between(line, '<arxiv_id>', '</arxiv_id>')
		print 'found arxiv_id = ' + arxiv_id
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

	if state == 1 and re.search('<publication>', line):
		publication= find_between(line, '<publication>', '</publication>')
		continue

	if state == 1 and re.search('<n_authors>', line):
		n_authors= find_between(line, '<n_authors>', '</n_authors>')
		continue

	if state == 1 and re.search('<author>', line):
		state= 2
		continue

	if state == 2 and re.search('<name>', line):
		name= find_between(line, '<name>', '</name>')
		authors.append(name)
		continue

	if state == 2 and re.search('<affiliation>', line):
		affiliation= find_between(line, '<affiliation>', '</affiliation>')
		affiliations.append(affiliation)
		continue

	if state == 2 and re.search('</author>', line):
		state= 1
		continue

	if state == 1 and re.search('</record>', line):
		for author in authors:
			for set_spec in set_specs:
				for affiliation in affiliations:
					my_str= arxiv_id + '\t'
					my_str+= set_spec + '\t'
					my_str+= created + '\t'
					my_str+= publication + '\t'
					my_str+= author + '\n'
					ofp.write(my_str)
		state= 0

ofp.close()
sys.exit(0)
