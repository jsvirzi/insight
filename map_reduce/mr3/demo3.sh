hdfs dfs -rm -R -f jsvirzi/mr3/out 
export HADOOP_HOME=/
python mr3.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr3/in -o hdfs:///user/ec2-user/jsvirzi/mr3/out >/dev/null
# python mr3.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr3/in -o hdfs:///user/ec2-user/jsvirzi/mr3/out 
