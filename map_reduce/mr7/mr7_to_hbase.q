DROP TABLE jsvirzi_mr7;
DROP TABLE jsvirzi_mr7_hive;
DROP TABLE jsvirzi_mr7_hbase;
DROP VIEW jsvirzi_mr7_hbaseview;

-- CREATE EXTERNAL TABLE IF NOT EXISTS jsvirzi_mr7 (author STRING, field STRING)
CREATE EXTERNAL TABLE jsvirzi_mr7 (author STRING, field STRING)
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
    LINES TERMINATED BY '\n' 
    stored as textfile 
    LOCATION '/user/ubuntu/jsvirzi/mr7/out';

DESCRIBE jsvirzi_mr7;

-- quit;

CREATE VIEW IF NOT EXISTS jsvirzi_mr7_hbaseview (author, field) AS 
    SELECT author, field 
    FROM jsvirzi_mr7;

-- Hive and HBase interaction using HBaseStorageHandler

-- quit;

-- CREATE EXTERNAL TABLE jsvirzi_mr7_hive (author STRING, field STRING)
CREATE TABLE jsvirzi_mr7_hive (author STRING, field STRING)
    STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
    WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key,metadata:field')
    TBLPROPERTIES ('hbase.table.name' = 'jsvirzi_mr7_hbase');

-- QUIT;

-- Stream data from Hive into HBase table

-- FROM jsvirzi_mr7_hbaseview INSERT INTO TABLE jsvirzi_mr7_hbase SELECT jsvirzi_mr7_hbaseview.*;
FROM jsvirzi_mr7 INSERT INTO TABLE jsvirzi_mr7_hive SELECT jsvirzi_mr7.*; 

