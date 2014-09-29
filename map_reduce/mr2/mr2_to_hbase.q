DROP TABLE jsvirzi_mr2;
DROP TABLE jsvirzi_mr2_hive;
DROP TABLE jsvirzi_mr2_hbase;
DROP VIEW jsvirzi_mr2_hbaseview;

-- CREATE EXTERNAL TABLE IF NOT EXISTS jsvirzi_mr2 (author STRING, field STRING)
CREATE EXTERNAL TABLE jsvirzi_mr2 (author STRING, field STRING)
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
    LINES TERMINATED BY '\n' 
    stored as textfile 
    LOCATION '/user/ec2-user/jsvirzi/mr2/out';

DESCRIBE jsvirzi_mr2;

-- quit;

CREATE VIEW IF NOT EXISTS jsvirzi_mr2_hbaseview (author, field) AS 
    SELECT author, field 
    FROM jsvirzi_mr2;

-- Hive and HBase interaction using HBaseStorageHandler

-- quit;

-- CREATE EXTERNAL TABLE jsvirzi_mr2_hive (author STRING, field STRING)
CREATE TABLE jsvirzi_mr2_hive (author STRING, field STRING)
    STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
    WITH SERDEPROPERTIES ('hbase.columns.mapping' = ':key,metadata:field')
    TBLPROPERTIES ('hbase.table.name' = 'jsvirzi_mr2_hbase');

-- QUIT;

-- Stream data from Hive into HBase table

-- FROM jsvirzi_mr2_hbaseview INSERT INTO TABLE jsvirzi_mr2_hbase SELECT jsvirzi_mr2_hbaseview.*;
FROM jsvirzi_mr2 INSERT INTO TABLE jsvirzi_mr2_hive SELECT jsvirzi_mr2.*; 

