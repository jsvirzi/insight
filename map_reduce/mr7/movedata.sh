hdfs dfs -rm -R -f /user/ubuntu/jsvirzi/mr7/out 
hdfs dfs -rm /user/ubuntu/jsvirzi/mr7/in/data.json
hdfs dfs -put ${1} /user/ubuntu/jsvirzi/mr7/in/data.json
