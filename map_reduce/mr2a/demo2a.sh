hdfs dfs -rm -R -f jsvirzi/mr2a/out 
export HADOOP_HOME=/
# python mr2a.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr2a/in -o hdfs:///user/ec2-user/jsvirzi/mr2a/out
python mr2a.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr2a/in -o hdfs:///user/ec2-user/jsvirzi/mr2a/out >/dev/null
