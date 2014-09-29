this job is used to simply place the raw data into hbase for query.
the row key is the arxiv document id

to use this, first setup (if not already done)

hdfs dfs -mkdir -p jsvirzi/mr2a/in
sh movedata.sh ~/jsvirzi/data/metadata.json (for debug, there are smaller
versions available of this file such as metadata_tiny.json)

for debugging, edit demo2a.sh and use the python / hadoop line that does not
output to /dev/null. There will be lots of output to the screen.

for production, edit demo2a.sh and use the python / hadoop line that outputs
to /dev/null to suppress the tons of output
