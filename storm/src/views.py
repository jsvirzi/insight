from flask import render_template, request
from app import app
from kafka import *
import time
import json

def make_graph(json_string):

	months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
	colors = ['orange', 'blue', 'red', 'purple', 'magenta', 'green', 'yellow', 'cyan']
	json_string = json_string.replace('\\', '')
	n = len(json_string)
	# json_string = json_string[1:n-1]

	print 'JSON STRING = ' + json_string

	docs = json.loads(json_string)
	dates = docs['citation_dates']
	author = docs['author']
	min_date = 999999
	max_date = 0
	for date in dates:
		my_list = date.split('-')
		year = int(my_list[0])
		month = int(my_list[1])
		a = year * 100 + month
		if a > max_date:
			max_date = a
		if a < min_date:
			min_date = a
	max_string = str(max_date)
	min_string = str(min_date)
	max_year = int(max_string[0:4])
	min_year = int(min_string[0:4])
	max_month = int(max_string[4:6])
	min_month = int(min_string[4:6])
	year = min_year
	month = min_month - 1
	axis_list = []
	while month < 12:
		my_str = months[month] + '-' + str(year)
		axis_list.append(my_str)
		month = month + 1

	year = year + 1

	while year < max_year:
		for month in range(0, 12):
			my_str = months[month] + '-' + str(year)
			axis_list.append(my_str)
		year = year + 1

	year = max_year
	for month in range(0, max_month):
		my_str = months[month] + '-' + str(year)
		axis_list.append(my_str)

	date_data = []
	for q in dates:
		my_list = q.split('-')
		year_str = my_list[0]
		month_str = my_list[1]
		i = int(month_str)
		my_str = months[i-1] + '-' + year_str
		date_data.append(my_str)

	counts = []
	for p in axis_list:
		n = date_data.count(p)
		counts.append(n)

	html = '<!DOCTYPE HTML>\n\n'
	html += '<html>\n'
	html += '<head>\n'
	html += '<script type="text/javascript" src="http://jsvirzi.dyndns.org/~jsvirzi/insight/canvasjs.min.js"></script>\n'
	html += '<script type="text/javascript">\n'
	html += 'window.onload = function () {\n'
	html += 'var chart = new CanvasJS.Chart("chartContainer",\n'
	html += '{ title:{text:"Citation History for ' + author + '"},\n'
	html += 'data: [ { type: "column", dataPoints: [\n'
	n = len(axis_list)
	j = 0
	k = len(colors)
	for i in range(0, n):
		date = axis_list[i]
		my_color = colors[j]
		my_color = 'red'
		j = j + 1
		if j >= k:
			j = 0
		html += '{ x: ' + str(i) + ', y : ' + str(counts[i]) + ', label:"' + date + '", color: "' + my_color + '"},\n'

	html += ']}\n'
	html += ']\n'
	html += '});\n'

	html += 'chart.render();\n'
	html += '}\n'
	html += '</script>\n'
	html += '</head>\n'

	html += '<body>\n'
	html += '<div id="chartContainer" style="height: 500px; width: 80%;"></div>\n'
	html += '</body>\n'
	html += '</html>\n'

	# print html

	return html

# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
	# Renders index.html.
	return render_template('index.html')

@app.route('/author')
def contact():
	# Renders author.html.
	return render_template('author.html')

@app.route('/rtquery/', methods=['GET'])
def rtquery():
	print 'Query invoked'
	author = str(request.args.get('author'))
	mykafka = KafkaClient('localhost:9092') 
	producer = SimpleProducer(mykafka) 
	print 'PROCESSING AUTHOR = [' + author + ']'
	producer.send_messages('citations_submit', author) 

	consumer = SimpleConsumer(mykafka, 'mygroup', 'citations_retrieve')
	messages = []
	delay = 0
	while len(messages) == 0:
	 	time.sleep(1)
	 	delay += 1
	 	print 'delay = ' + str(delay)
	 	messages = consumer.get_messages(count = 1, block = False)

	consumer.commit()
	mykafka.close()
	
	message = messages[0].message.value

	html = make_graph(message)

	# html = '<!DOCTYPE HTML>\n\n'
	# html += '<html>' + message + '</html>\n'

	return html 
	
