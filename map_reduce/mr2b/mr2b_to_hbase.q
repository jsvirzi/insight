DROP TABLE jsvirzi_mr2b;
DROP TABLE jsvirzi_mr2b_hive;
DROP TABLE jsvirzi_mr2b_hbase;
DROP VIEW jsvirzi_mr2b_hbaseview;

-- CREATE EXTERNAL TABLE IF NOT EXISTS jsvirzi_mr2b (author STRING, field STRING)
CREATE EXTERNAL TABLE jsvirzi_mr2b (author STRING, field STRING)
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
    LINES TERMINATED BY '\n' 
    stored as textfile 
    LOCATION '/user/ec2-user/jsvirzi/mr2b/out';

DESCRIBE jsvirzi_mr2b;

-- quit;

CREATE VIEW IF NOT EXISTS jsvirzi_mr2b_hbaseview (author, field) AS 
    SELECT author, field 
    FROM jsvirzi_mr2b;

-- Hive and HBase interaction using HBaseStorageHandler

-- quit;

-- CREATE EXTERNAL TABLE jsvirzi_mr2b_hive (author STRING, field STRING)
CREATE TABLE jsvirzi_mr2b_hive (author STRING, field STRING)
    STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
    WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key,metadata:field')
    TBLPROPERTIES ('hbase.table.name' = 'jsvirzi_mr2b_hbase');

-- QUIT;

-- Stream data from Hive into HBase table

-- FROM jsvirzi_mr2b_hbaseview INSERT INTO TABLE jsvirzi_mr2b_hbase SELECT jsvirzi_mr2b_hbaseview.*;
FROM jsvirzi_mr2b INSERT INTO TABLE jsvirzi_mr2b_hive SELECT jsvirzi_mr2b.*; 

