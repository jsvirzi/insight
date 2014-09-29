DROP TABLE jsvirzi_mr1;
DROP TABLE jsvirzi_mr1_hive;
DROP TABLE jsvirzi_mr1_hbase;
DROP VIEW jsvirzi_mr1_hbaseview;

-- CREATE EXTERNAL TABLE IF NOT EXISTS jsvirzi_mr1 (author STRING, field STRING)
CREATE EXTERNAL TABLE jsvirzi_mr1 (author STRING, field STRING)
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
    LINES TERMINATED BY '\n' 
    stored as textfile 
    LOCATION '/user/ec2-user/jsvirzi/mr1/out';

DESCRIBE jsvirzi_mr1;

-- quit;

CREATE VIEW IF NOT EXISTS jsvirzi_mr1_hbaseview (author, field) AS 
    SELECT author, field 
    FROM jsvirzi_mr1;

-- Hive and HBase interaction using HBaseStorageHandler

-- quit;

-- CREATE EXTERNAL TABLE jsvirzi_mr1_hive (author STRING, field STRING)
CREATE TABLE jsvirzi_mr1_hive (author STRING, field STRING)
    STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
    WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key,metadata:field')
    TBLPROPERTIES ('hbase.table.name' = 'jsvirzi_mr1_hbase');

-- QUIT;

-- Stream data from Hive into HBase table

-- FROM jsvirzi_mr1_hbaseview INSERT INTO TABLE jsvirzi_mr1_hbase SELECT jsvirzi_mr1_hbaseview.*;
FROM jsvirzi_mr1 INSERT INTO TABLE jsvirzi_mr1_hive SELECT jsvirzi_mr1.*; 

