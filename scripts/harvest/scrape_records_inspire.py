#!/usr/bin/python
import sys
import re
import os
from subprocess import call

# returns a list of strings between start and end delimiters
def split2(s, start, end): 
	len_s= len(s)
	len_start= len(start)
	len_end= len(end)
	temp= s
	list= []
	while True:
		my_first_index= temp.find(start)
		if my_first_index < 0:
			return list
		my_end_index= temp.find(end, my_first_index + len_start)
		if my_end_index < 0:
			return list
		list.append(temp[my_first_index + len_start : my_end_index])
		temp= temp[my_end_index + len_end : len_s]
	return list

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

inspire_id = '0'
arxiv_id = sys.argv[1]
ofile = sys.argv[2]

records_per_file = 25

base_url = 'http://inspirehep.net'

arxiv_id_url_encode = arxiv_id.replace('/', '%2F')

# general purpose temporary file 
tfile = 'tmp_' + arxiv_id.replace('/', '_') + '.html'

# this is just for finding the inspire record number corresponding to the arXiv entry
my_url = base_url + '/search?p=find+eprint+' + arxiv_id_url_encode + '&action17=Search'

# sys.exit(0)

print 'URL = ' + my_url
call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

# this is the string we are looking for: 
# <a class = "titlelink" href="/record/733349">LHC Signals from Warped Extra Dimensions</a>
lines = open(tfile)
my_line = ''
for line in lines:
	if re.search('titlelink', line) and re.search('href="/record/', line):
		inspire_id = find_between(line, 'href="/record/', '"')
		break
os.remove(tfile)

#
# *** begin REFERENCES ***
#
# search for references by the arxiv_id
i = 1

my_url = base_url + '/search?p=find+citedby+' + arxiv_id_url_encode + '&action10=Search'
my_url += '&amp;jrec=' + str(i) 

print 'URL = ' + my_url
call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

# the last line containing "records found" contains the number of references
lines = open(tfile)
n_refs = 0
my_list = []
for line in lines:
	if re.search('records found', line) and re.search('<strong>', line):
		my_str = find_between(line, '<strong>', '</strong>')
		if len(my_str):
			n_refs = int(my_str)
		print str(n_refs) + ' references found'
		if n_refs == 0:
			print 'WARNING condition exists in finding references by ' + arxiv_id
			print arxiv_id + ' apparently does not reference'
		if re.search('<a href="', my_line):
			my_list = line.split('<a href="')
		if len(my_list) == 1 and n_refs > records_per_file:
			print 'ERROR condition exists in finding references by' + arxiv_id
os.remove(tfile)

# harvest the references 
i = 1
my_refs = []
while i < n_refs:

	my_url= base_url + '/search?p=find+citedby+' + arxiv_id_url_encode + '&action10=Search'
	my_url+= '&amp;jrec=' + str(i)
	print 'wget ' + my_url
	call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

	i += records_per_file 

	lines= open(tfile)

	for line in lines:
		if re.search('titlelink', line):
			tstr = find_between(line, 'href="', '"')
			tlist = tstr.split('/')
			index = len(tlist)
			my_refs.append(tlist[index-1])
	
	os.remove(tfile)

verify_n_references = 'no'
if n_refs == len(my_refs):
	verify_n_references = 'yes'
#
# *** begin CITATIONS ***
#
# search for files citing the arXiv entry
i = 1

my_url= base_url + '/search?p=find+refersto+' + arxiv_id_url_encode + '&action10=Search'
my_url+= '&amp;jrec=' + str(i) 

print 'URL = ' + my_url
call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

# the last line containing "records found" contains the number of citations found 
lines = open(tfile)
n_cites = 0
my_list = []
for line in lines:
	if re.search('records found', line) and re.search('<strong>', line):
		my_str = find_between(line, '<strong>', '</strong>')
		if len(my_str):
			n_cites = int(my_str)
		print str(n_cites) + ' citations found'
		if n_cites == 0:
			print 'WARNING condition exists in finding citations to ' + arxiv_id
			print arxiv_id + ' apparently is never cited'
		if re.search('<a href="', my_line):
			my_list = line.split('<a href="')
		if len(my_list) == 1 and n_cites > records_per_file:
			print 'ERROR condition exists in finding citations to ' + arxiv_id
os.remove(tfile)

# harvest the citations
i = 1
my_cites = []
while i < n_cites:

	my_url= base_url + '/search?p=find+refersto+' + arxiv_id_url_encode + '&action10=Search'
	my_url+= '&amp;jrec=' + str(i)
	print 'wget ' + my_url
	call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

	i += records_per_file 

	lines= open(tfile)
	for line in lines:
		if re.search('titlelink', line):
			tstr = find_between(line, 'href="', '"')
			tlist = tstr.split('/')
			index = len(tlist)
			my_cites.append(tlist[index-1])
	
	os.remove(tfile)

verify_n_citations = 'no'
if n_cites == len(my_cites):
	verify_n_citations = 'yes'

if ofile != 'stdout':
	print 'appending data to ' + ofile

	fp = open(ofile, 'a')
	fp.write('<record>\n')
	fp.write('\t<arxiv_id>' + arxiv_id + '</arxiv_id>\n')
	fp.write('\t<inspire_id>' + inspire_id + '</inspire_id>\n')
	fp.write('\t<verify_n_references>' + verify_n_references + '</verify_n_references>\n')
	fp.write('\t<verify_n_citations>' + verify_n_citations + '</verify_n_citations>\n')

	if len(my_refs) > 0:
		fp.write('\t<n_references>' + str(len(my_refs)) + '</n_references>\n')
		for p in my_refs:
			fp.write('\t<reference>\n')
			fp.write('\t\t<inspire_id>' + p + '</inspire_id>\n')
			fp.write('\t</reference>\n')

	if len(my_cites) > 0:
		fp.write('\t<n_citations>' + str(len(my_cites)) + '</n_citations>\n')
		for p in my_cites:
			fp.write('\t<citation>\n')
			fp.write('\t\t<inspire_id>' + p + '</inspire_id>\n')
			fp.write('\t</citation>\n')

	fp.write('</record>\n')

	fp.close()

else:

	print '<record>'
	print '\t<arxiv_id>' + arxiv_id + '</arxiv_id>'
	print '\t<inspire_id>' + inspire_id + '</inspire_id>'
	print '\t<verify_n_references>' + verify_n_references + '</verify_n_references>'
	print '\t<verify_n_citations>' + verify_n_citations + '</verify_n_citations>'

	if len(my_refs) > 0:
		print '\t<n_references>' + str(len(my_refs)) + '</n_references>'
		for p in my_refs:
			print '\t<reference>'
			print '\t\t<inspire_id>' + p + '</inspire_id>'
			print '\t</reference>'

	if len(my_cites) > 0:
		print '\t<n_citations>' + str(len(my_cites)) + '</n_citations>'
		for p in my_cites:
			print '\t<citation>'
			print '\t\t<inspire_id>' + p + '</inspire_id>'
			print '\t</citation>'

	print '</record>'

