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
        title = docs['title']
        abstract = docs['abstract']
        arxiv_id = docs['arxiv_id']

        my_str = '{"author":['
        for author in authors:
            my_str += '"' + author + '"'
        # my_str = my_str.replace('""', '","')

        my_str += '],"affiliation":['
        for affiliation in affiliations:
            my_str += '"' + affiliation + '"'
        my_str = my_str.replace('""', '","')

        my_str += '],"arxiv_id":"' + arxiv_id + '"'

        my_str += ',"date":"' + date + '"'

        my_str += ',"title":"' + title + '"'

        my_str += ',"abstract":"' + abstract + '"}'

        yield arxiv_id, my_str 

    def blah(self):
        my_str = my_str.replace('""', '","')
        my_str += '],"arxiv_id":"' + arxiv_id + '","date":"' + date + '","title":"' + title + '","abstract":"' + abstract + '"}'

        # my_str = '{"author":"' + 'jsvirzi' + '","date":"' date + '"}'

        yield arxiv_id, my_str 

    def reducer(self, key, json_data_array):

        authors = []
        affiliations = []
        dates = []
        titles = []
        abstracts = []
        arxiv_ids = []
        i = 0
        for json_string in json_data_array:
            i = i + 1
            my_str = json_string
            my_str = my_str.replace('\\', '')
            json_data = json.loads(my_str)
            arxiv_id = json_data['arxiv_id']
            # date = json_data['date']
            # title = json_data['title']
            # abstract = json_data['abstract']
            affiliations = json_data['affiliation']
            authors = json_data['author']
            # dates.append(date)
            # titles.append(title)
            # abstracts.append(abstract)
            # arxiv_ids.append(arxiv_id)
            # affiliations.append(affiliation)
            # authors.append(author)

        # my_str = json_data_array[0] 
        yield key, my_str 

    def nullstuff(self):
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
        str += '"' + date + '"],'

        str += '"title":['
        n = len(titles)
        for i in range(0, n-1):
            title = titles[i]
            str += '"' + title + '",'
        title = titles[n-1]
        str += '"' + title + '"],'

        str += '"abstract":['
        n = len(abstracts)
        for i in range(0, n-1):
            abstract = abstracts[i]
            str += '"' + abstract + '",'
        abstract = abstracts[n-1]
        str += '"' + abstract + '"]}'

        yield key, str 

if __name__ == '__main__':
    MRWordFrequencyCount.run()

