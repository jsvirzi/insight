hdfs dfs -rm -R -f jsvirzi/mr2b/out 
hdfs dfs -rm jsvirzi/mr2b/in/data.json
hdfs dfs -put ${1} jsvirzi/mr2b/in/data.json
