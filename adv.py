#!/usr/bin/env python
import json
import hashlib
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

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

story = MongoClient()['adv']['story']

def renderWelcome():
	welcomeTitle = ''
	return pageTemplate % (
		boxTemplate % (
			welcomeTitle,
			'<div style="margin: 2em; overflow: hidden;">\
			adventure?'
			+ buttonTemplate % ('start', 'begin') + '</div>'))

def processSubmit(origin, request):

	if request == '':
		return False

	try:
		origin = ObjectId(origin)
	except:
		pass

	originChapter = story.find_one({'_id': origin})

	for option in originChapter['options']:
		if option['text'] == request:
			return True

	newChapter = story.insert_one(
		{
			'options': [],
			'text': ''
		}
	)

	result = story.update_one(
		{'_id': origin},
		{
			'$push': {
				'options': {
					'destination': newChapter.inserted_id,
					'text': request,
					'creator': True
				}
			}
		}
	)

	print(result)
	print(result.acknowledged)
	print(result.matched_count)
	print(result.modified_count)
	print(originChapter)

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

	try:
		scene = ObjectId(scene)
	except:
		pass

	chapter = story.find_one({'_id': scene})

	if chapter is None:
		return 'oops, \"' + scene + '\" doesn\t appear to be in the story\
			<br/>\
			<a href="/adv">go back?</a>';

	options = ''
	for option in chapter['options']:
		if story.find_one({'_id': option['destination']})['text'] != '':
			options += optionTemplate % (
				option['destination'], option['text'])
		else:
			options += suggTemplate % (option['text'])

	outString = outString % (chapter['text'], options, scene)

	return outString

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
