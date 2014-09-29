from __future__ import absolute_import, print_function # , unicode_literals

import itertools
from streamparse.spout import Spout
from kafka import * 

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

class WordSpout(Spout):

	def initialize(self, stormconf, context):
		self.mykafka = KafkaClient('localhost:9092') 
		self.consumer = SimpleConsumer(self.mykafka, 'mygroup', 'mytopic') 
		# self.words = itertools.cycle(['dog', 'cat', 'zebra', 'elephant'])

	def next_tuple(self):
		messages = self.consumer.get_messages(count=1, block=False) 
		for message in messages:
			my_str = str(message)
			# my_str = find_between('value
			my_str = find_between(my_str, 'value=', ')')
			my_str = my_str[1:-1]
			my_str = 'PROCESSING [' + my_str + ']\n'
        		self.log(my_str)
			self.emit([my_str])
		
		# if len(messages):
			# self.emit([messages[0]])

