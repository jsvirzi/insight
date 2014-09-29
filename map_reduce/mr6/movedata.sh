hdfs dfs -rm -R -f jsvirzi/mr6/out 
hdfs dfs -rm -R -f jsvirzi/mr6/in
hdfs dfs -mkdir jsvirzi/mr6/in
hdfs dfs -put ${1}/* jsvirzi/mr6/in
