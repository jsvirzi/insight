#!/usr/bin/python
import re
import sys
from subprocess import call
import urllib
import happybase
import json

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

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

def get_citation_dates(arxiv_id):

    new_list = []

    base_url = 'http://adsabs.harvard.edu/cgi-bin'
    my_url = base_url + '/bib_query?arXiv:' + arxiv_id
    tfile = 'tmp.html'
    print 'URL = ' + my_url
    call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

    ads_id = '0'
    lines = open(tfile)
    for line in lines:
	    if re.search('adsabs.harvard.edu/adsabs/abs/', line):
		    ads_id = find_between(line, 'adsabs.harvard.edu/adsabs/abs/', '"')
		    print 'ADS ID = ' + ads_id

    my_url = 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=' + ads_id + '&amp;refs=CITATIONS&amp;db_key=PHY'
    print 'URL = ' + my_url
    call(['wget', my_url, '-O', tfile, '-o', '/dev/null'])

    lines = open(tfile)
    for line in lines:
        if re.search('ABSTRACT', line) and re.search('<tr>', line) and re.search('</tr>', line) and re.search('bibcode', line):
            inspire_id = find_between(line, 'name="bibcode" value="', '">')
            # print 'INSPIRE ID = %s' % inspire_id
            my_list = split2(line, '>', '<')
            for my_str in my_list:
                if len(my_str) == 7 and my_str[2:3] == '/':
                    # print 'ELEMENT = %s with LENGTH = %d. POS=%s ' % (my_str, len(my_str), my_str[2:3])
                    tmp_list = my_str.split('/')
                    if len(tmp_list) >= 2:
                        month = tmp_list[0]
                        year = tmp_list[1]
                        print 'DATE = %s-%s' % (year, month)
                        new_list.append(year + '-' + month)
                        # sys.stdin.read(1) 

    return new_list

# main
		
connection = happybase.Connection('localhost') 
table = connection.table('jsvirzi_mr1_hbase') 
author = sys.argv[1] 
ofile = sys.argv[2]
# author = 'Virzi J.'
row = table.row('"' + author + '"') 

my_str = row['metadata:field'] 
my_str = my_str.replace('\\', '')
n = len(my_str)
my_str = my_str[1:n-1]
print my_str
docs = json.loads(my_str)
arxiv_ids = docs['arxiv_id']
n = len(arxiv_ids)
print 'length = %d' % n

date_list = []
for i in range(0, n):
    arxiv_id = arxiv_ids[i]
    print 'arxiv_id %d = %s' % (i, arxiv_id)
    tmp_list = get_citation_dates(arxiv_id)
    date_list = date_list + tmp_list

print 'FINAL DATES'
json_string = '{"author":"' + author + '","citation_dates":['
for p in date_list:
    json_string += '"' + p + '"'
    print p
json_string = json_string.replace('""', '","')
json_string += ']}\n'
fp = open(ofile, 'a')
fp.write(json_string)
fp.close()
sys.exit(0)
