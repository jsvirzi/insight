from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
from subprocess import call
import subprocess

import re
import sys
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

    ofile = '/home/ubuntu/tmp.joe'
    fp = open(ofile, 'a')
    fp.write('boo 1 ' + ' ' + arxiv_id)
    fp.close()

    output = subprocess.Popen(['wget', my_url, '-O', '-', '-o', '/dev/null'], \
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

    ofile = '/home/ubuntu/tmp2.joe'
    fp = open(ofile, 'w')
    fp.write(my_url)
    fp.close()

    lines = output.split('\n')
    ads_id = '0'
    for line in lines:
	    if re.search('adsabs.harvard.edu/adsabs/abs/', line):
		    ads_id = find_between(line, 'adsabs.harvard.edu/adsabs/abs/', '"')

    ofile = '/home/ubuntu/tmp2a.joe'
    fp = open(ofile, 'w')
    fp.write(ads_id)
    fp.close()

    my_url = 'http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=' + ads_id + '&amp;refs=CITATIONS&amp;db_key=PHY'
    output = subprocess.Popen(['wget', my_url, '-O', '-', '-o', '/dev/null'], \
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

    lines = output.split('\n')

    ofile = '/home/ubuntu/tmp3.joe'
    fp = open(ofile, 'w')
    fp.write(my_url)
    for line in lines:
    	fp.write(line + '\n')
    fp.close()

    for line in lines:
        if re.search('ABSTRACT', line) and re.search('<tr>', line) and re.search('</tr>', line) and re.search('bibcode', line):
            inspire_id = find_between(line, 'name="bibcode" value="', '">')
            my_list = split2(line, '>', '<')
            for my_str in my_list:
                if len(my_str) == 7 and my_str[2:3] == '/':
                    tmp_list = my_str.split('/')
                    if len(tmp_list) >= 2:
                        month = tmp_list[0]
                        year = tmp_list[1]
                        new_list.append(year + '-' + month)

    ofile = '/home/ubuntu/tmp4.joe'
    fp = open(ofile, 'w')
    # fp.write(output)
    fp.write('here i am')
    fp.close()

    return new_list

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        author = tup.values[0]

	author = 'Virzi J.'

	ofile = '/home/ubuntu/tmp.joe'
	fp = open(ofile, 'a')
	fp.write(author)
	fp.close()

	connection = happybase.Connection('ec2-54-183-207-177.us-west-1.compute.amazonaws.com') 
	table = connection.table('jsvirzi_mr1_hbase') 
	row = table.row('"' + author + '"') 

	my_str = row['metadata:field'] 
	my_str = my_str.replace('\\', '')

	n = len(my_str)
	my_str = my_str[1:n-1]
	docs = json.loads(my_str)
	arxiv_ids = docs['arxiv_id']
	n = len(arxiv_ids)

	ofile = '/home/ubuntu/tmp.joe'
	fp = open(ofile, 'a')
	fp.write('boo 1 ' + str(n) + ' ' + arxiv_ids[0])
	fp.close()

	date_list = []
	for i in range(0, n):
    		arxiv_id = arxiv_ids[i]
    		tmp_list = get_citation_dates(arxiv_id)
    		date_list = date_list + tmp_list

	json_string = '{"author":"' + author + '","citation_dates":['
	for p in date_list:
    		json_string += '"' + p + '"'

	json_string = json_string.replace('""', '","')
	json_string += ']}\n'

	ofile = '/home/ubuntu/tmp4.joe'
	fp = open(ofile, 'a')
	fp.write(json_string)
	fp.close()

	connection = happybase.Connection('ec2-54-183-207-177.us-west-1.compute.amazonaws.com') 
	table = connection.table('jsvirzi_mr6_realtime_hbase') 
	my_str = '\'' + json_string + '\''
	table.put('\'' + author + '\'', {'metadata:field':my_str})
	
        self.counts[word] += 1
        self.emit([word, self.counts[word]])
        self.log('%s: %d' % (word, self.counts[word]))

