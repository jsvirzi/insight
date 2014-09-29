# python harvest_metadata.py ../arxiv_metadata_dump_20140906/physics_969.html >xxx_969

start=${1}
if [ "${start}" == "" ] ; then start="1"; fi
skip=${2}
if [ "${skip}" == "" ] ; then skip="1"; fi
datestamp=20140906
odir="../metadata_${datestamp}"
mkdir -p ${odir}
idir="../arxiv_metadata_dump_${datestamp}"
files=`ls ${idir}/physics_*.html`
cdir="../citation_data"
tdir="../citation_data_inspire"
for((i=${start};i<970;i+=${skip})) do
	ifile="physics_${i}.html"
	ofile="${odir}/citations_arxiv_${i}.xml"
	echo "${ifile} => ${ofile}"
	# python harvest_citations_inspire.py ${ifile} >${ofile}
	echo "python harvest_citations_inspire.py ${idir} ${ifile} ${cdir} ${tdir} >${ofile}"
	python harvest_citations_inspire.py ${idir} ${ifile} ${odir} ${cdir} ${tdir} >${ofile}
	echo "sh ${odir}/arxiv_${i}.html.sh"
	sh ${odir}/arxiv_${i}.html.sh

done
