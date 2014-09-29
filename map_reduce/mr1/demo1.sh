hdfs dfs -rm -R -f jsvirzi/mr1/out 
export HADOOP_HOME=/
# python mr1.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr1/in -o hdfs:///user/ec2-user/jsvirzi/mr1/out
python mr1.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ec2-user/jsvirzi/mr1/in -o hdfs:///user/ec2-user/jsvirzi/mr1/out >/dev/null
