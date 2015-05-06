#!/usr/bin/env python
import json

pageTemplate = """
<html>
<head>
	<link rel="stylesheet" type="text/css" href="/adv.css">
	<meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' name='viewport'/>
	<script src="/adv.js"></script>
	<title>adv</title>
</head>
<body>
	<div id="contentContainer">
		<div id="bgTopColor"></div>
		<div id="bgTitleColor"></div>
		<div id="title">%s</div>
		<div id="content">
			<div id="addOption">
				<div id="addOptionButton" onclick="userCreateAction()">
					<div id="addIcon" class="addOptionButtonIcon">
					</div>
					<div id="editIcon" class="addOptionButtonIcon">
					</div>
					<div id="sendIcon" class="addOptionButtonIcon">
					</div>
				</div>
				<div id="addOptionTextBox">add your own action</div>
				<textarea id="actionEntry" placeholder="do something..." required></textarea>
			</div>
			%s
			<hr/>
			%s
		</div>
	</div>
</body>
</html>
"""

storyTemplate = """
<div id="storyBox">
	%s
</div>
"""

optionTemplate = """
<div class="optionBox" onclick="selectOption('%s')">
	%s
</div>
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
	return [
		str.encode(
			pageTemplate % ("name of previous action",
				(storyTemplate % "something happens...<br/>possibly long<br/>with many lines<br/>...<br/>...<br/>yep"),
				((optionTemplate % ("test1", "do something"))
				+ (optionTemplate % ("test2","do something else"))
				+ (optionTemplate % ("test3","do yet another thing")))))
		]

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
