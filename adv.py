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
	<div id="page">
		<div id="bgTopColor"></div>
		<div id="bgTitleColor"></div>
		%s
	</div>
</body>
</html>
"""

boxTemplate = """
<div id="titleBox">%s</div>
<div id="content">%s</div>
"""

buttonTemplate = """
<div class="button" onclick="gotoPage('%s')">%s</div>
"""

storyTemplate = """
<div id="storyBox">
	%s
</div>
<hr/>
%s
<div id="newChoiceContainer" class="optionBox">
	<div id="newChoiceSubmit" class="button" onclick="userCreateChoice()">Submit</div>
	<div id="newChoiceEntryContainerContainer">
		<div id="newChoiceEntryContainer">
			<form id="userSubmitChoice" method="post" action="/adv/submit">
				<input name="choice" id="newChoiceEntry" type="text" placeholder="do something else?">
			</form>
		</div>
	</div>
</div>
"""

optionTemplate = """
<div class="optionBox clickable" onclick="selectOption('%s')">
	%s
</div>
"""

def renderWelcome():
	welcomeTitle = 'hmmm...'
	return pageTemplate % (
		boxTemplate % (
			welcomeTitle, '<div style="margin: 2em;">' + buttonTemplate % (
				'start', 'begin') + 'a bunch of text that says stuff</div>'))

def renderStory(title = False, story = False, options = False):
	return pageTemplate % (boxTemplate % ("title", storyTemplate % ("story",
		optionTemplate % ("test1", "do something") +
		optionTemplate % ("test2", "do something else") +
		optionTemplate % ("test3", "do yet antoher thing")
		)))

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
	#return [str.encode(renderWelcome())]
	return [str.encode(renderStory("test"))]

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
