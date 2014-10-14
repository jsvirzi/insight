from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
import json
import happybase

class MRWordFrequencyCount(MRJob):

    def mapper_init(self):

        connection = happybase.Connection('localhost')
        self.table = connection.table('jsvirzi_mr3_hbase')

    def reducer_init(self):
        self.fpr = open('reduce.out', 'w')

    def reducer_final(self):
        self.fpr.close()

    def mapper(self, _, line):

        tlines = line.split('\t');
        if len(tlines) != 1:
            tline = tlines[1].replace('\\"', '"')
        else:
            tline = tlines[0].replace('\\"', '"')
        if tline[0] == '"':
            tline = tline[1:-1]

        # n = input('debug')
        # print 'incoming = [' + tline + ']'

        docs1 = json.loads(tline)
        collaborators1 = docs1['collaborators']
        author = docs1['author']
        collaborators1.append(author)
        n = len(collaborators1)
        if n <= 10:
            for collaborator1 in collaborators1: 
                # print 'collaborator 1 = ' + collaborator1
                row = self.table.row('"' + collaborator1 + '"')
                try:
                    tline = row['metadata:field']
                    tline = tline[1:-1]
                    tline = tline.replace('\\"', '"')
                except:
                    continue

                # print 'stage2 = [' + tline + ']'
                docs2 = json.loads(tline)
                collaborators2 = docs2['collaborators']
                author = docs2['author']
                collaborators2.append(author)
                for collaborator2 in collaborators2: 
                    if collaborator1 != collaborator2:
                        # print 'yield: [' + collaborator1 + '] with value: [' + collaborator2 + ']'
			# n = input('hello')
                        yield collaborator1, collaborator2 

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

        self.fpr.write(my_str + '\n')

        yield key, my_str 

if __name__ == '__main__':
    MRWordFrequencyCount.run()

