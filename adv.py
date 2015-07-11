#!/usr/bin/env python
import json
import hashlib

pageTemplate = """
<html>
<head>
	<link rel="stylesheet" type="text/css" href="/static/style.css">
	<meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' name='viewport'/>
	<script src="/static/script.js"></script>
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
			<form id="userSubmitChoice" method="post" action="%s/submit">
				<input name="choice" id="newChoiceEntry" type="text" placeholder="do something else?" required>
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

suggTemplate = """
<div class="optionBoxInvalid">
	%s
</div>
"""

adv = None;

def renderWelcome():
	welcomeTitle = ''
	return pageTemplate % (
		boxTemplate % (
			welcomeTitle,
			'<div style="margin: 2em; overflow: hidden;">\
			adventure?'
			+ buttonTemplate % ('start', 'begin') + '</div>'))

def processSubmit(origin, request):
	if not origin in adv:
		adv[origin] = {
			'options': [ ]
		}

	for option in adv[origin]['options']:
		if option['text'] == request:
			return True

	newItemHash = hashlib.md5(str.encode(origin + request)).hexdigest()

	adv[newItemHash] = {
		'text': '',
		'options': [
		]
	}

	adv[origin]['options'].append(
		{
			'text': request,
			'destination': newItemHash,
			'creator': True,
		})

	advFileWrite = open('/srv/adv/story.json', 'w')
	json.dump(adv, advFileWrite, indent=4)
	advFileWrite.close()


	return True;

def renderSubmit(request, backLoc):
	outString = pageTemplate % boxTemplate;
	outString = outString % ('request submitted',
		'<div style="padding: 1em; font-size: 1.2em; overflow: hidden;"> \
		you\'re request to:\
		<div style="color: #444; font-size: 1.5em; text-align:center;">'
		+ request + '</div> \
		has been submitted'
		+ buttonTemplate % (backLoc, 'back') + '</div>')

	return outString

def renderStory(scene):
	outString = pageTemplate % boxTemplate;
	outString = outString % ('', storyTemplate)

	if not scene in adv:
		return 'oops, \"' + scene + '\" doesn\t appear to be in the story\
			<br/>\
			<a href="/adv">go back?</a>';

	advScene = adv[scene]

	choices = ''
	for option in advScene['options']:
		if option['destination'] in adv \
				and (adv[option['destination']]['text'] != ''):
			choices += optionTemplate % (
				option['destination'], option['text'])
		else:
			choices += suggTemplate % option['text']

	outString = outString % (advScene['text'], choices, scene)

	return outString

def loadAdvFile():
	global adv

	try:
		advFile = open('/srv/adv/story.json', 'r')
	except:
		return False;

	advString = advFile.read()
	advFile.close()

	#parse json
	adv = json.loads(advString)

	#it got this far, it probably worked
	return adv != None;

def explodeUrl(url):
	if len(url) > 1:
		if url[0] == '/':
			url = url[1:]

		if url[-1] == '/':
			url = url[:-1]

	urlParts = ['']

	for c in url:
		if c == '/':
			urlParts.append('')
		else:
			urlParts[-1] = urlParts[-1] + c;

	return urlParts;

def application(environ, start_response):
	start_response('200 OK', [('Content-Type','text/html')])

	if not loadAdvFile():
		return [u'couldn\'t load required files, internal server error i guess, 500?']

	path = explodeUrl(environ.get('PATH_INFO', ''))

	if  path[0] == '':
		return [str.encode(renderWelcome())]
	elif len(path) >= 2 and path[1] == 'submit':
		submitedData = b''

		try:
			length = int(environ.get('CONTENT_LENGTH', '0'))
		except ValueError:
			length = 0

		if length != 0:
			submitedData = environ['wsgi.input'].read(length)

		submitedData = submitedData.decode("utf-8") \
			.replace('choice=', '') \
			.replace('+', ' ')

		result = processSubmit(path[0], submitedData)
		if result != True:
			return [str.encode('oh no')];

		return [str.encode(renderSubmit(submitedData, path[0]))]
	else:
		return [str.encode(renderStory(path[0]))]
