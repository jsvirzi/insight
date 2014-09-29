hdfs dfs -rm -R -f jsvirzi/mr2a/out 
hdfs dfs -rm jsvirzi/mr2a/in/data.json
hdfs dfs -put ${1} jsvirzi/mr2a/in/data.json
