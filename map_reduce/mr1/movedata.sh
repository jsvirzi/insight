hdfs dfs -rm -R -f jsvirzi/mr1/out 
hdfs dfs -rm jsvirzi/mr1/in/data.json
hdfs dfs -put ${1} jsvirzi/mr1/in/data.json
