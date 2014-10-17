from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
import json
import happybase

class MRWordFrequencyCount(MRJob):

    def mapper_init(self):
        connection = happybase.Connection('localhost')
        self.table = connection.table('jsvirzi_mr3_hbase')
        self.mofile = '/home/ubuntu/jsvirzi/insight/map_reduce/mr7/mapper.out'
        self.fpm = open(self.mofile, 'w')
        self.map_cntd = 1000
        self.map_cntr = self.map_cntd 
        self.map_total = 0

    def mapper_final(self):
        self.fpm.close()

    def reducer_init(self):
        self.rofile = '/home/ubuntu/jsvirzi/insight/map_reduce/mr7/reducer.out'
        self.fpr = open(self.rofile, 'w')

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

        self.map_cntr = self.map_cntr - 1
        self.map_total = self.map_total + 1
        if self.map_cntr == 0:
            self.map_cntr = self.map_cntd 
            self.fpm.close()
            self.fpm = open(self.mofile, 'a')
            print 'processing line %d' % self.map_total

        docs0 = json.loads(tline)
        authors = docs0['authors']
        n = len(authors)
        if n > 10:
            return

        for author in authors:
            # author = 'Virzi J.'
            row = self.table.row('"' + author + '"')
            try:
                tline = row['metadata:field']
                tline = tline[1:-1]
                tline = tline.replace('\\"', '"')
            except:
                continue
            docs1 = json.loads(tline)
            collaborators1 = docs1['collaborators']
            tmp_author = docs1['author']
            collaborators1.append(tmp_author)
            for collaborator1 in collaborators1: 
                # print 'collaborator 1 = ' + collaborator1
                row = self.table.row('"' + collaborator1 + '"')
                try:
                    tline = row['metadata:field']
                    tline = tline[1:-1]
                    tline = tline.replace('\\"', '"')
                except:
                    continue
                docs2 = json.loads(tline)
                collaborators2 = docs2['collaborators']
                tmp_author = docs2['author']
                collaborators2.append(tmp_author)
                for collaborator2 in collaborators2: 
                    if author != collaborator2:
                        # print 'YIELD: ' + author + ' ' + collaborator2
                        yield author, collaborator2

        return

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

