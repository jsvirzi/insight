hdfs dfs -rm -R -f jsvirzi/mr2/out 
export HADOOP_HOME=/
# python mr2.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr2/in -o hdfs:///user/ec2-user/jsvirzi/mr2/out
python mr2.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr2/in -o hdfs:///user/ec2-user/jsvirzi/mr2/out >/dev/null
