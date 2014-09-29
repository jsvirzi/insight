#!/usr/bin/python
import sys
import re
from subprocess import call
import glob
import os

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

# arxiv metadata dump directory
idir= sys.argv[1]
# which file
iname= sys.argv[2]
# metadata target directory
odir= sys.argv[3]
# everything is currently in cdir
cdir= sys.argv[4]
# everything should be in target dir
tdir= sys.argv[5]
ifile= idir + '/' + iname

# to move the files from cdir to tdir after tarring them
script_file= iname.replace('physics', 'arxiv')
script_file= odir + '/' + script_file + '.sh'
script_fp= open(script_file, 'w')
tar_file= tdir + '/' + iname.replace('physics', 'arxiv') + '.tar'

print 'script file = ' + script_file

# correct the name of the input metadata file
tfile= ifile.replace('physics', 'arxiv')
script_fp.write('mv -i ' + ifile + ' ' + tfile + '\n')
script_fp.write('cp -i ' + tfile + ' ' + ifile + '\n')
script_fp.write('tar -cvf ' + tar_file + ' ' + tfile + '\n')

my_state= 0
my_refs= []
lines= open(ifile)
for line in lines:
	if my_state == 0 and re.search('<record>', line):
		my_state= 1
		my_refs= []
		continue

	if my_state == 1 and re.search('<id>', line):
		my_id= find_between(line, '<id>', '</id>')

	if my_state == 1 and re.search('</record>', line):
		ifile= cdir + '/entry_' + my_id + '.html'
		tfile= tdir + '/' + os.path.basename(ifile)
		script_fp.write('mv -i ' + ifile + ' ' + tfile + '\n')
		# script_fp.write('mv -i ' + ifile + ' ' + tdir + '/\n');
		script_fp.write('tar --append --file ' + tar_file + ' ' + tfile + '\n')
		print '<record>'
		print '\t<arxiv_id>' + my_id + '</arxiv_id>'
		
		my_refs= []
		tstr= cdir + '/cited_by_' + my_id + '.*.html'
		ifiles= glob.glob(tstr)
		for ifile in ifiles:
			tfile= tdir + '/' + os.path.basename(ifile)
			script_fp.write('mv -i ' + ifile + ' ' + tfile + '\n')
			script_fp.write('tar --append --file ' + tar_file + ' ' + tfile + '\n')
			# script_fp.write('mv -i ' + ifile + ' ' + odir + '/\n');
			tlines= open(ifile)
			for tline in tlines:
				if re.search('titlelink', tline):
					tstr= find_between(tline, 'href="', '"')
					tlist= tstr.split('/')
					index= len(tlist)
					my_refs.append(tlist[index-1])

		if len(my_refs) > 0:
			print '\t<n_references>' + str(len(my_refs)) + '</n_references>'
			for p in my_refs:
				print '\t<reference>'
				print '\t\t<inspire_id>' + p + '</inspire_id>'
				print '\t</reference>'

		print '</record>'
		my_state= 0

		# script_fp.close()
		# sys.exit(0)

script_fp.close()
