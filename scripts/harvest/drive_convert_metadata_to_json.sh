wdir="../metadata_20140906_abstracts"
files=`ls -1 ${wdir}/metadata_*.xml`
clean=${1}
tfile=${wdir}/metadata.json
rm -Rf ${tfile}
for file in ${files}; do
	odir=`dirname ${file}`
	ifile=`basename ${file}`
	str=`basename ${file} .xml`
	index=`echo ${str} | cut -b 10-`

	ofile=${odir}/metadata_${index}.json
	if [ "${clean}" = "clean" ] ; then 
		echo "removing ${ofile}"
		rm -f ${ofile}; 
	fi
	if [ ! -e ${ofile} ] ; then
		echo ${ifile} ${ofile} ${index}
		echo "python convert_metadata_xml_to_json.py ${wdir}/metadata_${index}.xml ${ofile}"
		python convert_metadata_xml_to_json.py ${wdir}/metadata_${index}.xml ${ofile}
		cat ${ofile} >>${tfile}
	fi

	# ofile=${odir}/citation_data_${index}_ads.json
	# if [ ! -e ${ofile} ] ; then
		# echo ${ifile} ${ofile} ${index}
		# echo "python convert_citation_data_ads_xml_to_json.py ../citation_data_ads/citation_data_ads_${index}"
		# python convert_citation_data_ads_xml_to_json.py ../citation_data_ads/citation_data_ads_${index}.json
	# fi
done
