from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
import json

class MRWordFrequencyCount(MRJob):

# write output as JSON
    # OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, line):
        docs = json.loads(line)
        authors = docs['authors']
        n = len(authors)
        if n <= 10:
            for author_key in authors: 
                for author_val in authors: 
                    if author_key != author_val:
                        yield author_key, author_val 

    def reducer(self, key, values):

        my_list = []
        for viter in values:
            my_list.append(viter)

        collaborator_set = set(my_list)
        collaborators = list(collaborator_set)

        my_str = '{"author":"' + key + '","collaborators":['
        n = len(collaborators)
        for i in range(0, n-1):
            collaborator = collaborators[i]
            my_str += '"' + collaborator + '",'
        collaborator = collaborators[n-1]
        my_str += '"' + collaborator + '"],'

        my_str += '"frequency":['
        n = len(collaborators)
        for i in range(0, n-1):
            collaborator = collaborators[i]
            cnt = my_list.count(collaborator)
            my_str += '"' + str(cnt) + '",'
        collaborator = collaborators[n-1]
        cnt = my_list.count(collaborator)
        my_str += '"' + str(cnt) + '"]}'
        
        my_str = my_str.replace('\\\"', '"')
        yield key, my_str 

if __name__ == '__main__':
    MRWordFrequencyCount.run()

