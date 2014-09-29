hdfs dfs -rm -R -f jsvirzi/mr3/out 
hdfs dfs -rm jsvirzi/mr3/in/data.json
hdfs dfs -put ${1} jsvirzi/mr3/in/data.json
