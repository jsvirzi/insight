# python harvest_metadata.py ../arxiv_metadata_dump_20140906/physics_969.html >xxx_969

start=${1}
if [ "${start}" == "" ] ; then start="1"; fi
skip=${2}
if [ "${skip}" == "" ] ; then skip="1"; fi
datestamp=20140906
odir="../metadata_${datestamp}_abstracts"
mkdir -p ${odir}
idir="../arxiv_metadata_dump_${datestamp}"
files=`ls ${idir}/physics_*.html`
for((i=${start};i<970;i+=${skip})) do
	ifile="${idir}/physics_${i}.html"
# output xml file
	xfile="${odir}/metadata_${i}.xml"
	echo "python harvest_metadata.py ${ifile} ${xfile}"
	python harvest_metadata.py ${ifile} ${xfile}
done
