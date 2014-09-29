DROP TABLE jsvirzi_mr6;
DROP TABLE jsvirzi_mr6_hive;
DROP TABLE jsvirzi_mr6_hbase;
DROP VIEW jsvirzi_mr6_hbaseview;

-- CREATE EXTERNAL TABLE IF NOT EXISTS jsvirzi_mr6 (author STRING, field STRING)
CREATE EXTERNAL TABLE jsvirzi_mr6 (author STRING, field STRING)
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
    LINES TERMINATED BY '\n' 
    stored as textfile 
    LOCATION '/user/ec2-user/jsvirzi/mr6/out';

DESCRIBE jsvirzi_mr6;

-- quit;

CREATE VIEW IF NOT EXISTS jsvirzi_mr6_hbaseview (author, field) AS 
    SELECT author, field 
    FROM jsvirzi_mr6;

-- Hive and HBase interaction using HBaseStorageHandler

-- quit;

-- CREATE EXTERNAL TABLE jsvirzi_mr6_hive (author STRING, field STRING)
CREATE TABLE jsvirzi_mr6_hive (author STRING, field STRING)
    STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
    WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key,metadata:field')
    TBLPROPERTIES ('hbase.table.name' = 'jsvirzi_mr6_hbase');

-- QUIT;

-- Stream data from Hive into HBase table

-- FROM jsvirzi_mr6_hbaseview INSERT INTO TABLE jsvirzi_mr6_hbase SELECT jsvirzi_mr6_hbaseview.*;
FROM jsvirzi_mr6 INSERT INTO TABLE jsvirzi_mr6_hive SELECT jsvirzi_mr6.*; 

