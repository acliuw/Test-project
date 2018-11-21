import requests
import subprocess
import json


class GHBot:
	def __init__(self, username, oauthToken):
		self.username = username;
		self.oauthToken = oauthToken;
		self.authHeaders = {'Authorization': 'token %s' % oauthToken, 'Accept': 'application/vnd.github.v3+json'};


	## This method is called after every 'event', such as when someone comments. 
	## data is the JSON data describing the event. 
	## Currently a stub. 
	def update(self, data):
		print("GHBot.update called")
		print(data)
		pass


	## This is called after each event. The bot should determine how to react to the current state
	## of the repository. 
	## Right now, the bot always responds with a fixed message. 
	def react(self, data): 
		print("GHBot.react called")

		# Don't respond to your own posts (or it'll be an endless cycle)
		if data["comment"]["user"]["login"] != self.username:
			self.respond("UPF", data)

		
	def respond(self, symlog, data): 
		print("GHBot.respond", symlog, "called")
		
		url = data['issue']['url']
		self.create_issue_comment_with_url(url, symlog)




##================== ISSUES ===================##
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

#ghbot = GHBot("acliuw", "90ad3fbbfb6ed3c3bc8d30a395d9430fb1aff5ae")
#ghbot.create_issue_comment("https://api.github.com/repos/acliuw/Test-project/", 1, "This message was automatically generated")
#ghbot.create_issue("https://api.github.com/repos/acliuw/Test-project", "I have an issue!", "This issue was created by a bot.")
#ghbot.open_issue("https://api.github.com/repos/acliuw/Test-project", 2)




