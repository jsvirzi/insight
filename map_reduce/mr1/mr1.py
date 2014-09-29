from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
import json

class MRWordFrequencyCount(MRJob):

# write output as JSON
    # OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        docs = json.loads(line)
        authors = docs['authors']
        affiliations = docs['affiliations'];
        date = docs['date']
        arxiv_id = docs['arxiv_id']
        n = len(authors)
        for i in range(0, n):
            author = authors[i]
            affiliation = affiliations[i] 
            str = '{"author":"' + author + '","arxiv_id":"' + arxiv_id + '","date":"' + date + '","affiliation":"' + affiliation + '"}'
            yield author, str 

    def reducer(self, key, json_data_array):
        authors = []
        affiliations = []
        dates = []
        arxiv_ids = []
        for json_string in json_data_array:
            json_data = json.loads(json_string)
            arxiv_id = json_data['arxiv_id']
            date = json_data['date']
            affiliation = json_data['affiliation']
            author = json_data['author']
            dates.append(date)
            arxiv_ids.append(arxiv_id)
            affiliations.append(affiliation)
            authors.append(author)

        str = '{"arxiv_id":['
        n = len(arxiv_ids)
        for i in range(0, n-1):
            arxiv_id = arxiv_ids[i]
            str += '"' + arxiv_id + '",'
        arxiv_id = arxiv_ids[n-1]
        str += '"' + arxiv_id + '"],'

        str += '"author":['
        n = len(authors)
        for i in range(0, n-1):
            author = authors[i]
            str += '"' + author + '",'
        author = authors[n-1]
        str += '"' + author + '"],'

        str += '"affiliation":['
        n = len(affiliations)
        for i in range(0, n-1):
            affiliation = affiliations[i]
            str += '"' + affiliation + '",'
        affiliation = affiliations[n-1]
        str += '"' + affiliation + '"],'

        str += '"date":['
        n = len(dates)
        for i in range(0, n-1):
            date = dates[i]
            str += '"' + date + '",'
        date = dates[n-1]
        str += '"' + date + '"]}'

        yield key, str 

if __name__ == '__main__':
    MRWordFrequencyCount.run()

