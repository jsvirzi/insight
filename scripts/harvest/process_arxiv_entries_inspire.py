#!/usr/bin/python
import sys
import re
from subprocess import call

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

state = 0
ifile = sys.argv[1]
ofile = sys.argv[2]
lines = open(ifile)
for line in lines:
	if state == 0 and re.search('<record>', line):
		state = 1
		continue

	if state == 1 and re.search('<arxiv_id>', line):
		arxiv_id = find_between(line, '<arxiv_id>', '</arxiv_id>')
		continue

	if state == 1 and re.search('<set_spec>', line):
		str = find_between(line, '<set_spec>', '</set_spec>')
		if re.search('physics', str.lower()) and not re.search('astro-ph', str.lower()):
			print './scrape_records_inspire.py ' + arxiv_id + ' ' + ofile
			call(['./scrape_records_inspire.py', arxiv_id, ofile])
			state = 2
		continue
		
	if re.search('</record>', line):
		state = 0
		continue

	print '*** WARNING: unknown state ***'

sys.exit(0)

