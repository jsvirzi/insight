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
		n_references= 0
		references= []
		continue

	if state == 1 and re.search('<arxiv_id>', line):
		arxiv_id= find_between(line, '<arxiv_id>', '</arxiv_id>')
		print 'found arxiv_id = ' + arxiv_id
		continue

	if state == 1 and re.search('<n_references>', line):
		n_references= find_between(line, '<n_references>', '</n_references>')
		continue

	if state == 1 and re.search('<reference>', line):
		state= 2
		continue

	if state == 2 and re.search('<ads_id>', line):
		ads_id= find_between(line, '<ads_id>', '</ads_id>')
		references.append(ads_id)
		state= 3
		continue

	if state == 3 and re.search('</reference>', line):
		state= 1
		continue

	if state == 1 and re.search('</record>', line):
		ofp.write('{"arxiv_id":"' + arxiv_id + '", "references":[')
		n= len(reference)
		for i in range(0, n-1):
			ofp.write('"' + references[i] + '",')
		ofp.write('"' + references[n-1] + '"]}\n')
		state= 0

ofp.close()
sys.exit(0)
