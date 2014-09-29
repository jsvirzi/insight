from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
import json

class MRWordFrequencyCount(MRJob):

# write output as JSON
    # OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        docs = json.loads(line)
        arxiv_id = docs['arxiv_id']
        yield arxiv_id, line 

    def reducer(self, key, json_data_array):

        my_str = '{"author":"N/A","arxiv_id":"N/A"}'
        for json_string in json_data_array:
            my_str = json_string

        yield key, my_str 

if __name__ == '__main__':
    MRWordFrequencyCount.run()

