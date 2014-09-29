#!/usr/bin/python
import sys
import re
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

def canonical(str):
	list = str.split(' ')
	name = list[0]
	for i in range(1, len(list)):
        	t = list[i].split('.')
        	for j in range(0, len(t)):
			p = t[j]
			if len(p) == 0:
				continue
			elif len(p) == 1:
				name += ' ' + p + '.'
			else:
				q = p.replace(p[1:], '.')
				name += ' ' + q

	name = name.replace('\'', '')
	name = name.replace(',', '')

	my_str = find_between(name, '&', ';')
	if len(my_str) > 0:
		my_str = '&' + my_str + ';'
		name = name.replace(my_str, '')

	return name

ifile= sys.argv[1]
# output xml file
xfile= sys.argv[2]
# output tab delimited value
# ofile= sys.argv[3]

# ofp= open(ofile, 'a')
xfp= open(xfile, 'a')

my_state = -1 
lines = open(ifile)
my_authors = []
my_set_specs = []
my_affiliations = []
my_doi = ''
my_title = ''
my_created = ''
my_id = ''
my_publication = 'none'
my_datestamp = ''
my_uberline = ''
my_abstract = ''
for line in lines:

	if re.search('<record>', line):
		if my_state != 0 and my_state != -1:
			print 'ERROR: inconsistency in record'
		my_state = 1
		my_authors = []
		my_set_specs = []
		my_affiliations = []
		my_doi = ''
		my_title = ''
		my_created = ''
		my_id = ''
		my_publication = 'none'
		my_datestamp = ''
		my_abstract = ''
		my_uberline = line
		continue

	if my_state == 1:
		my_uberline += line
		if re.search('</record>', line):
			my_state = 0
		if my_state != 0:
			continue

	if my_state == -1:
		continue

	my_uberline = my_uberline.replace('\n', '')
	my_uberline = my_uberline.replace('\r', '')
	my_uberline = my_uberline.replace('  ', ' ')
	my_uberline = my_uberline.replace('&quot;', '')
	my_uberline = my_uberline.replace('\'', '')
	my_uberline = my_uberline.replace('"', '')

	# print 'LINE = [' + my_uberline + ']'
	# sys.exit(0)

	if my_state == 0 and re.search('<id>', my_uberline):
		my_id = find_between(my_uberline, '<id>', '</id>')

	if my_state == 0 and re.search('setSpec', my_uberline):
		my_set_spec = find_between(my_uberline, '<setSpec>', '</setSpec>')
		my_set_specs.append(my_set_spec)

	if my_state == 0 and re.search('<created>', my_uberline):
		my_created = find_between(my_uberline, '<created>', '</created>')

	if my_state == 0 and re.search('<datestamp>', my_uberline):
		my_datestamp = find_between(my_uberline, '<datestamp>', '</datestamp>')

	if my_state == 0 and re.search('<abstract>', my_uberline):
		my_abstract = find_between(my_uberline, '<abstract>', '</abstract>')

	if my_state == 0 and re.search('<title>', my_uberline):
		my_title = find_between(my_uberline, '<title>', '</title>')

	if my_state == 0 and re.search('<journal-ref>', my_uberline):
		my_publication = find_between(my_uberline, '<journal-ref>', '</journal-ref>')

	if my_state == 0 and re.search('<doi>', my_uberline):
		my_doi = find_between(my_uberline, '<doi>', '</doi>')

	if my_state == 0 and re.search('<authors>', my_uberline):
		my_list= split2(my_uberline, '<author>', '</author>')
		for p in my_list:
			my_keyname = find_between(p, '<keyname>', '</keyname>')
			my_forenames = split2(p, '<forenames>', '</forenames>')
			my_author = my_keyname
			for q in my_forenames:
				my_author+= ' ' 
				my_author+= q 
			# print 'author = ' + my_author,
			my_author = canonical(my_author)
			# print ' canonical = [' + my_author + ']'
			my_authors.append(my_author)
			my_list = split2(p, '<affiliation>', '</affiliation>')
			if len(my_list) == 0:
				my_list = ['NONE']
			my_affiliations.append(my_list)

	xstr= '<record>\n'
	xstr+= '\t<arxiv_id>' + my_id + '</arxiv_id>\n'
	if len(my_set_specs):
		n_set_specs = len(my_set_specs)
		xstr += '\t<n_set_specs>' + str(n_set_specs) + '</n_set_specs>\n'
		xstr += '\t<set_specs>\n'
		for my_set_spec in my_set_specs:
			xstr += '\t\t<set_spec>' + my_set_spec + '</set_spec>\n'
		xstr += '\t</set_specs>\n'
	if len(my_created):
		xstr += '\t<created>' + my_created + '</created>\n'
	if len(my_datestamp):
		xstr += '\t<datestamp>' + my_datestamp + '</datestamp>\n'
	if len(my_title):
		xstr += '\t<title>' + my_title + '</title>\n'
	if len(my_abstract):
		xstr += '\t<abstract>' + my_abstract + '</abstract>\n'
	if len(my_doi):
		xstr += '\t<doi>' + my_doi + '</doi>\n'
	if len(my_publication):
		xstr += '\t<publication>' + my_publication + '</publication>\n'
	n_authors= len(my_authors)
	xstr+= '\t<n_authors>' + str(n_authors)  + '</n_authors>\n'
	xstr+= '\t<authors>\n'
	for my_index in range(0, n_authors):
		xstr += '\t\t<author>\n'
		p = my_authors[my_index]
		xstr += '\t\t\t<name>' + p + '</name>\n'
		for p in my_affiliations[my_index]:
			xstr += '\t\t\t<affiliation>' + p + '</affiliation>\n'
		xstr += '\t\t</author>\n'
	xstr+= '\t</authors>\n'
	xstr+= '</record>\n'
	# print xstr
	xfp.write(xstr)
	my_state = 0

# ofp.close()
xfp.close()
sys.exit(0)
