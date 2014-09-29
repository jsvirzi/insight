ofile="metadata.json"
files=`ls metadata_*json`
for file in ${files}; do
	echo "${file}"
	cat ${file} >>${ofile}
done
