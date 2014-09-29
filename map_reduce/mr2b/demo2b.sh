hdfs dfs -rm -R -f jsvirzi/mr2b/out 
export HADOOP_HOME=/
# python mr2b.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr2b/in -o hdfs:///user/ec2-user/jsvirzi/mr2b/out
python mr2b.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr2b/in -o hdfs:///user/ec2-user/jsvirzi/mr2b/out >/dev/null
