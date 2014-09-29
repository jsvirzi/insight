from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
import json

class MRWordFrequencyCount(MRJob):

# write output as JSON
    # OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        docs = json.loads(line)
        author = docs['author']
        my_str = '{"author":"' + author + '","citation_dates":['
        citation_dates = docs['citation_dates']
        for date in citation_dates:
            my_str += '"' + date + '"'
        my_str = my_str.replace('""', '","')
        my_str += ']}'

        yield author, my_str 

    def reducer(self, key, citation_dates_list):

        my_str = '{"author":"' + key + '","citation_dates":['
        for json_string in citation_dates_list:
            docs = json.loads(json_string)
            citation_dates = docs['citation_dates']
            for date in citation_dates:
                my_str += '"' + date + '"'
        my_str = my_str.replace('""', '","')
        my_str += ']}'

        if key != '0':
            yield key, my_str 

if __name__ == '__main__':
    MRWordFrequencyCount.run()

