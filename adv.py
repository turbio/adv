#!/usr/bin/env python
import json

htmlTemplate = """
<html>
<head>
<link rel="stylesheet" type="text/css" href="adv.css">
</head>
<body>
<div>test</div>
</body>
</html>
"""

def printScene(scene):
	outString = ''
	outString = outString + adventure[scene]['text'] + '\n'
	for option in adventure[scene]['options']:
		outString = outString + option + ' -> ' + adventure[scene]['options'][option] + '\n'
	outString = outString + adventure[scene]['options'] + '\n'

def application(environ, start_response):
	#load adventure file
	try:
		advFile = open('/srv/adv/story.json', 'r')
	except:
		start_response('200 OK', [('Content-Type','text/html')])
		return [b'hmmm... looks like the story file can\'t be open']

	advString = advFile.read()
	advFile.close()

	#parse json
	adventure = json.loads(advString)

	start_response('200 OK', [('Content-Type','text/html')])
	#return [b'Hello World']
	return [str.encode(htmlTemplate)]

	# build the response body possibly using the environ dictionary
	#response_body = 'The request method was %s' % environ['REQUEST_METHOD']
	
	# HTTP response code and message
	#status = '200 OK'

	# These are HTTP headers expected by the client.
	# They must be wrapped as a list of tupled pairs:
	# [(Header name, Header value)].
	#response_headers = [('Content-Type', 'text/plain'),
		#('Content-Length', str(len(response_body)))]

	# Send them to the server using the supplied function
	#start_response(status, response_headers)

	# Return the response body.
	# Notice it is wrapped in a list although it could be any iterable.
	#return [response_body]
