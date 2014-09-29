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

base_url= 'http://adsabs.harvard.edu/cgi-bin'

entry_arxiv = sys.argv[1]

my_url= base_url + '/bib_query?arXiv:' + entry_arxiv
ofile= 'entry_' + entry_arxiv.replace('/', '_') + '.html'
 
# print 'URL = ' + my_url
call(['wget', my_url, '-O', ofile])

my_url= ''
lines= open(ofile)
for line in lines:
	if re.search('REFERENCES IN THE ARTICLE', line.upper()):
		# print line
		my_str= find_between(line, 'href="', '"')
		my_url= my_str.replace('&#38;', '&amp;')
		# print '(2) URL = ' + my_url

file_index= 1
obase= 'cited_by_'
ofile= obase + entry_arxiv.replace('/', '_') + '.' + str(file_index) + '.html'
# print '(3) URL = ' + my_url
call(['wget', my_url, '-O', ofile])

my_refs= []
lines= open(ofile)
for line in lines:
	if re.search('name="bibcode"', line) and re.search('href', line):
		# print line
		my_name= find_between(line, 'value="', '"')
		my_name= my_name.replace('&amp;', '&')
		my_url= find_between(line, 'href="', '"')
		my_str= '\t<reference>\n'
		my_str+= '\t\t<ads_id>' + my_name + '</ads_id>\n'
		# print 'URL = ' + my_url
		# to get the arxiv_id from the ads_id uncomment the next lines w/##
		## ofile= 'temp_' + entry_arxiv.replace('/', '_') + '.tmp'
		## call(['wget', my_url, '-O', ofile])
		## tlines= open(ofile)
		## for tline in tlines:
			## if re.search('arXiv e-print', tline) and re.search('href', tline):
				## my_arxiv_name= find_between(tline, '(arXiv:', ')')
				## if len(my_arxiv_name):
					## my_str+= '\t\t<reference_arxiv_id>' + my_arxiv_name + '</reference_arxiv_id>\n'
		my_str+= '\t</reference>\n'
		my_refs.append(my_str)
		# call(['rm', '-f', ofile])

print '<record>'
print '\t<arxiv_id>' + entry_arxiv + '</arxiv_id>'
print '\t<n_references>' + str(len(my_refs)) + '</n_references>'
for p in my_refs:
	print p,
print '</record>'

sys.exit(0)
