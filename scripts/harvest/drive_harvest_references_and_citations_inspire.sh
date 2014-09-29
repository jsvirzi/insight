# python harvest_metadata.py ../arxiv_metadata_dump_20140906/physics_969.html >xxx_969

start=${1}
if [ "${start}" == "" ] ; then start="1"; fi
skip=${2}
if [ "${skip}" == "" ] ; then skip="1"; fi
clean=${3}
datestamp=20140906
idir="../metadata_${datestamp}"
odir="../metadata_${datestamp}"

# files=`ls ${idir}/metadata_*.xml`
for((i=${start};i<970;i+=${skip})) do
	ifile="${idir}/metadata_${i}.xml"
	ofile="${odir}/references_citations_${i}.xml"
	lfile="${odir}/log_${i}"
	if [ "${clean}" == "clean" ] ; then 
		# rm ${ofile}; 
		# rm ${lfile}; 
		echo "starting clean for ${i}";
	fi
	if [ -e ${ofile} ] ; then 
		# echo ${ofile} exists; 
		continue;
	fi
	echo "python process_arxiv_entries_inspire.py ${ifile} ${ofile}"
	# python process_arxiv_entries_inspire.py ${ifile} ${ofile} >${lfile}

done

ofile="${odir}/references_citations.json"
rm -f ${ofile} # files are concatenated
for((i=${start};i<970;i+=${skip})) do
	ifile="${odir}/references_citations_${i}.xml"
	echo "python convert_references_and_citations_inspire_xml_to_json.py ${ifile} ${ofile}"
	python convert_references_and_citations_inspire_xml_to_json.py ${ifile} ${ofile}
done
