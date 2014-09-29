hdfs dfs -rm -R -f jsvirzi/mr2/out 
hdfs dfs -rm jsvirzi/mr2/in/data.json
hdfs dfs -put ${1} jsvirzi/mr2/in/data.json
