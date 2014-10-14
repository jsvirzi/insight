hdfs dfs -rm -R -f /user/ubuntu/jsvirzi/mr7/out 
export HADOOP_HOME=/
# python mr7.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ubuntu/jsvirzi/mr7/in -o hdfs:///user/ubuntu/jsvirzi/mr7/out >/dev/null
python mr7.py -r hadoop --hadoop-bin /usr/bin/hadoop hdfs:///user/ubuntu/jsvirzi/mr7/in -o hdfs:///user/ubuntu/jsvirzi/mr7/out 
# standalone
python mr7.py ~/jsvirzi/data/mr7/in_merged/part-merged_00000_00013
