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

ifile= sys.argv[1]
lines= open(ifile)
my_id= -1
my_state= 0
lines= open(ifile)
for line in lines:
	if my_state == 0 and re.search('<record>', line):
		my_state= 1
		my_id= ''
		my_set_spec= ''
		continue
	elif my_state == 2 and re.search('</record>', line):
		my_state= 0
		continue

	if my_state == 1 and re.search('<id>', line):
		my_id= find_between(line, '<id>', '</id>')

	if my_state == 1 and re.search('<setSpec>', line):
		my_set_spec= find_between(line, '<setSpec>', '</setSpec>')

	if my_state == 1 and len(my_id) > 0 and len(my_set_spec) > 0:
		# print 'arxiv_id=' + my_id + ' set_spec=' + my_set_spec
		my_state= 2
		if re.search('astro-ph', my_set_spec):
			# print 'call ' + my_id + ' ' + my_set_spec
			call(['./scrape_records_ads.py', my_id])
		
sys.exit(0)



ifile= sys.argv[1]
lines= open(ifile)
for line in lines:
	if re.search('identifier', line):
		my_str= find_between(line, '<identifier>oai:arXiv.org:', '</identifier>')
		print './scrape_records.py ' + my_str
		call(['./scrape_records.py', my_str])

sys.exit(0)














records_per_file= 25

base_url= 'http://inspirehep.net'

entry_arxiv = sys.argv[1]

mystr= 'http://inspirehep.net/search?p=find+eprint+' + entry_arxiv + '&action17=Search'

print 'original = ' + mystr

# import urllib
# res=urllib.quote(entry_arxiv)
entry_arxiv_url_encode= entry_arxiv.replace('/', '%2F', 1)

print entry_arxiv_url_encode 

# sys.exit(0)

# string='<small>HEP : <strong>72</strong> records found &nbsp; 1 - 25<a href="/search?ln=en&amp;p=find+citedby+hep-ph%2F0612015&amp;jrec=26" class="img"><img src="/img/sn.gif" alt="next" border="0" /></a><a href="/search?ln=en&amp;p=find+citedby+hep-ph%2F0612015&amp;jrec=48" class="img"><img src="/img/se.gif" alt="end" border="0" /></a><input type="hidden" name="p" value="find citedby hep-ph/0612015" /><input type="hidden" name="cc" value="HEP" /><input type="hidden" name="f" value="" /><input type="hidden" name="sf" value="" /><input type="hidden" name="so" value="d" /><input type="hidden" name="of" value="hb" /><input type="hidden" name="rg" value="25" /><input type="hidden" name="as" value="0" /><input type="hidden" name="ln" value="en" /><input type="hidden" name="p1" value="" /><input type="hidden" name="p2" value="" /><input type="hidden" name="p3" value="" /><input type="hidden" name="f1" value="" /><input type="hidden" name="f2" value="" /><input type="hidden" name="f3" value="" /><input type="hidden" name="m1" value="" /><input type="hidden" name="m2" value="" /><input type="hidden" name="m3" value="" /><input type="hidden" name="op1" value="" /><input type="hidden" name="op2" value="" /><input type="hidden" name="sc" value="0" /><input type="hidden" name="d1y" value="0" /><input type="hidden" name="d1m" value="0" /><input type="hidden" name="d1d" value="0" /><input type="hidden" name="d2y" value="0" /><input type="hidden" name="d2m" value="0" /><input type="hidden" name="d2d" value="0" /><input type="hidden" name="dt" value="" />&nbsp; jump to record: <input type="text" name="jrec" size="4" value="1" /></small></div></form>'

# this is just for finding the inspire record number corresponding to the arXiv entry
my_url= base_url + '/search?p=find+eprint+' + entry_arxiv_url_encode + '&action17=Search'
print 'url encode = ' + my_url

# search for files citing the arXiv entry
i= 1
file_index= 1
obase= 'cited_by_'
ofile= obase + entry_arxiv.replace('/', '_', 1) + '.' + str(file_index) + '.html'
file_index+= 1
i += records_per_file

my_url= base_url + '/search?p=find+citedby+' + entry_arxiv_url_encode + '&action10=Search'
my_url+= '&amp;jrec=' + str(i) 

print 'URL = ' + my_url

# sys.exit(0)

print 'ofile = ' + ofile
call(['wget', my_url, '-O', ofile])

n_refs= -1
print 'the last string is :'
print 'string = ' + my_line

# sys.exit(0)

string= my_line

nrefs=find_between(string, '<strong>', '</strong>')
print 'nrefs = ' + nrefs

my_list=string.split('<a href="')

# print my_list[1]

my_index=my_list[1].find('&amp;jrec=')

# print '%s%d' %('my index = ', my_index)

rel_url=my_list[1][0:my_index]

last=int(nrefs)
while i<last:

	# print '%s%d%s%d' %('refs = ', i, '/', last)
	ofile= obase + entry_arxiv.replace('/', '_', 1) + '.' + str(file_index) + '.html'
	file_index+= 1
	my_url= base_url + '/search?p=find+citedby+' + entry_arxiv_url_encode + '&action10=Search'
	my_url+= '&amp;jrec=' + str(i)
	print 'wget ' + my_url
	call(['wget', my_url, '-O', ofile])
	# print '%s%s%s%s%s%s' %('wget "', base_url, rel_url, '&amp;jrec=', str(i), '"') 
	i += records_per_file 

