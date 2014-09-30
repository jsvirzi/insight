Trackademix
===========

[Trackademix](http://trackademix.com) was developed as my project for [Insight Data Science](http://insightdataengineering.com) September through October 2014.

## Intro

**Trackademix** tracks scientific contributions and collaborations and portrays a more detailed picture 
than the standard author-document-date, author-document-date, etc. approach can. 
**Trackademix** examines the web of collaborators with whom a particular author has worked over the years.
This paints a broader picture than a simple listing of the co-authors on any given document.

Furthermore, as an author publishes his work, its relevance is typically determined by the number of citations made thereto.
A simple count of the citations is not as informative as examining a chronological history of the citations.
For example, two authors may have been cited 300 times over the last five years.
The first author had one paper cited 250 times and two others cited 25 times each.
The second author has six (6) papers cited 50 times each.
The citation profile is very different in both cases; **Trackademix** allows us to visualize the citation history. 
**TrackademiX** application harvests available information from the [ArXiv](http://arxiv.org), 
[INSPIRE HEP](http://inspirehep.net) and 
[NASA ADS](http://adsabs.harvard.edu) databases, 
filters out information unlikely to be part of the author''s scientific contributions history

## The Data Pipeline

![Alt Text](https://github.com/jsvirzi/insight/blob/master/images/pipeline.png "Data Pipeline")

The pipeline has a batch component, which is intended to be processed weekly (specifically on Sunday).
The batch processing retrieves metadata information from the ArXiv via a REST API.
If recent works have cited older works, the records are updated in our database.
The batch component is intended to have eventual consistency on a *weekly* timescale.

The pipeline has two real-time components, both of which use STORM to process the requests.
The first real-time component scans the ArXiv records for recent activity,
and performs informational updates to a temporary database.
This temporary database is eventually superceded by the database created during the batch processing.
The second real-time component is an on-demand query which will take process the information when the user clicks
the ''submit'' button in the User Interface.

# Batch 

The details of the data pipeline for the batch process are as follows:

- Kafka is used to collect data coming from RESTful API calls
- A custom web crawler harvests information from Kafka and scrapes additional information from different web-based databases
(ADS, INSPIRE, etc.)
- Relevant information is filtered and subsequently stored into HDFS
- PIG is used to merge information from the different databases stored in HDFS 
- MR Job Python scripts are used to process the different query variables using Map/Reduce algorithms
- Hive is used to import the MapReduce jobs into HBase
- Flask serves to query HBase and send the results as HTML/JavaScript pages to the browser

# Real-Time

The real-time data pipeline shares the same data collection technology as the batch process,
except that it has been implemented with STORM.
- Kafka feeds the ''spouts''
- The STORM ''bolts'' perform the scraping
- The ''bolts'' use Happybase to deliver the results into HBase
- Flask serves to query HBase and send the results as HTML/JavaScript pages to the browser

# On-Demand

The real-time data pipeline can be used to service on-demand queries via the user interface
