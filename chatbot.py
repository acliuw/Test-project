import requests
import subprocess
import json
from MarkovModel import *

class GHBot:
	def __init__(self, username):
		self.username = username;
		self.oauthToken = self.loadAuthToken().strip();
		self.authHeaders = {'Authorization': 'token %s' % self.oauthToken, 'Accept': 'application/vnd.github.v3+json'};
		
		# The current responses are randomly generated.
		self.markovModels = [MarkovModel("textdata/one-star-amazon-video-games.txt"), MarkovModel("textdata/five-star-amazon-video-games.txt"),MarkovModel("textdata/trump-speeches.txt"),MarkovModel("textdata/trump-tweets.txt")]
		self.currentPersonality = 0 # Default is negative Amazon game reviews

	## - Update the internal state of the bot. 
	## - Called after every time a comment is posted.
	## - data is the JSON data describing the event. 
	## - ** Currently a stub. 

	def update(self, data):
		print("GHBot.update called")

		try:
			last_comment = self.get_last_comment(data).strip()
			print(last_comment)
		except:
			return
			
		if last_comment == "negative amazon":
			self.currentPersonality = 0
			print("Switching to negative amazon reviews")
		elif last_comment == "positive amazon":
			self.currentPersonality = 1
			print("Switching to positive amazon reviews")
		elif last_comment == "trump speeches":
			self.currentPersonality = 2
			print("Switching to Trump speeches")
		elif last_comment == "trump tweets":
			self.currentPersonality = 3
			print("Switching to Trump tweets")


	## - The bot should decide how to react to each event. 
	## - data is the JSON data describing the event.  
	## - Currently responds with a randomly generated phrase from a Markov model.

	def react(self, data): 
		print("GHBot.react called")

		# Don't respond to your own posts (or it'll be an endless cycle)

		try:
			if data["comment"]["user"]["login"] != self.username:
				self.respond("UPF", data)
		except:
			print("Unknown request format")

	
	## - Responds to a comment with a random Markov generated comment. 

	def respond(self, symlog, data): 
		print("GHBot.respond", symlog, "called")
		

		url = data['issue']['url']

		message = "" 
		for i in range(3):
			message += self.markovModels[self.currentPersonality].generateMarkovChain() + " "

		# message = self.get_last_comment(data) ### This makes the bot respond with the last message on the thread.
		 
		# print(self.get_all_comments_on_issue(data))

		self.create_issue_comment_with_url(url, message)

	## - Load the bot's auth token from a file. 
	## - DO NOT COMMIT THE AUTH TOKEN FILE (git ignore it). 

	def loadAuthToken(self):
		authToken = open(self.username, "r").read()
		return authToken



##================== UTILITIES ===================##
	def create_issue_comment_with_url(self, url, message):
		postURL = "%s/comments" %(url)
		r = requests.post(postURL, headers = self.authHeaders, data = json.dumps({ "body": message }))

		if r.status_code == 201:
			print("Success")
		else:
			print("POST request failed")
			print(r)

	def create_issue_comment_with_id(self, repoURL, issueID, message):
		if repoURL[-1] == "/":
			repoURL = repoURL[:-1]
		postURL = "%s/issues/%d/comments" %(repoURL, issueID)
		r = requests.post(postURL, headers = self.authHeaders, data = json.dumps({ "body": message }))
		
		if r.status_code == 201:
			print("Success")
		else:
			print("POST request failed")
			print(r)

	def create_issue(self, repoURL, title, body = ""):
		if repoURL[-1] == "/":
			repoURL = repoURL[:-1]
		postURL = "%s/issues" %(repoURL)

		data = {
			"title": title,
			"body": body
		}

		r = requests.post(postURL, headers = self.authHeaders, data = json.dumps(data))

		if r.status_code == 201:
			print("Success")
		else:
			print("POST request failed")
			print(r)

	def close_issue(self, repoURL, issueID):
		if repoURL[-1] == "/":
			repoURL = repoURL[:-1]
		postURL = "%s/issues/%d" %(repoURL, issueID)

		data = {
			"state": "closed"
		}

		r = requests.patch(postURL, headers = self.authHeaders, data = json.dumps(data))

		if r.status_code == 200:
			print("Success")
		else:
			print("POST request failed")
			print(r)

	def open_issue(self, repoURL, issueID):
		if repoURL[-1] == "/":
			repoURL = repoURL[:-1]
		postURL = "%s/issues/%d" %(repoURL, issueID)

		data = {
			"state": "open"
		}

		r = requests.patch(postURL, headers = self.authHeaders, data = json.dumps(data))

		if r.status_code == 200:
			print("Success")
		else:
			print("POST request failed")
			print(r)

	def get_last_comment(self, data):
		r = requests.get(data['comment']['url'], headers = self.authHeaders)

		if r.status_code == 200:
			print("Success")
			return r.json()['body']
		else:
			print("GET request failed")
			print(r)		
#r = requests.get(data['issue']['url'], 

	def get_all_comments_on_issue(self, data):
		r = requests.get(data['issue']['url'] + "/comments", headers = self.authHeaders)

		if r.status_code == 200:
			print("Success")
			return r.json()
		else:
			print("GET request failed")
			print(r)





