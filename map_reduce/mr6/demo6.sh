hdfs dfs -rm -R -f jsvirzi/mr6/out 
export HADOOP_HOME=/
# python mr6.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr6/in -o hdfs:///user/ec2-user/jsvirzi/mr6/out
python mr6.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr6/in -o hdfs:///user/ec2-user/jsvirzi/mr6/out >/dev/null
