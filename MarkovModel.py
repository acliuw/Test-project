import re
import json
import nltk
from random import *


class MarkovModel:
	def __init__(self, file):
		self.file = file
		self.wordMap = dict()
		self.train(file)

	def train(self,file):
		text = open(file, "r").read()
		self.analyze(text)

		# data = json.loads(text)

		# for tweet in data["payload"]:
		# 	self.analyzeTweet(tweet['text'])



		#sentences = re.findall('.*[.*!*\?*]', text)
		#print(sentences)

	def analyze(self, text):
		tokens = nltk.word_tokenize(text)
		tokens = list(filter(lambda x: len(x) > 0 and x != "(" and x != ")" and x!= '&' and x != "quot", tokens))
		print("%d tokens loaded."% len(tokens))

		last1 = "START1"
		last2 = "START2"


		for token in tokens:
			self.updateWord(last1, last2, token)

			if token == "." or token == "!" or token == "?":
				last1 = "START1"
				last2 = "START2"
			else:
				last1 = last2
				last2 = token
		

	def analyzeTweet(self,tweet):
		tweet += " "
		tweet = tweet.replace(",", "")
		tweet = tweet.replace("\"", "")
		tweet = tweet.replace("\'", "")
		tweet = tweet.replace("\n", " ")
		tweet = tweet.replace("&amp;", "&")

		tweet = tweet.replace(".", " . ")
		tweet = tweet.replace(" ! ", " ! ")
		tweet = tweet.replace(" ? ", " ? ")

		#tweet = tweet.replace(". ", " . END START1 START2 ")
		#tweet = tweet.replace("! ", " ! END START1 START2 ")
		#tweet = tweet.replace("? ", " ? END START1 START2 ")

		tweet = "START1 START2 " + tweet 
		if tweet[-14:] == "START1 START2 ":
			tweet = tweet[:-14]

		words = tweet.split(" ")
		words = list(filter(lambda x: len(x) > 0 and ("http" not in x) and ("co" not in x), words))
		if words[-1] != "END":
			words.append("END")

		for i in range(len(words)-2):
			a = words[i]
			b = words[i+1]
			c = words[i+2]

			self.updateWord(a, b, c)

	def updateWord(self, a, b, c):
		if (a,b) not in self.wordMap:
			self.wordMap[(a,b)] = dict()
			self.wordMap[(a,b)][c] = 1
		elif c not in self.wordMap[(a,b)]:
			self.wordMap[(a,b)][c] = 1
		else:
			self.wordMap[(a,b)][c] += 1

	def generateMarkovChain(self):
		currentA = "START1"
		currentB = "START2"
		message = ""
		while True:
			nextW = self.nextWord(currentA, currentB)

			if nextW in [".","!","?"]:
				if len(message) > 0 and message[-1] == " ":
					message = message[:-1] + nextW + " "
				else:
					message += nextW + " "
				break
			elif nextW == "," or nextW[0] == "\'" or nextW == "n\'t": 
				message = message[:-1] + nextW + " "
			elif nextW == "’":
				message = message[:-1] + nextW
			else:
				message += nextW + " "
			currentA = currentB
			currentB = nextW

		if len(message) < 5:
			return self.generateMarkovChain()
		return message

	def nextWord(self,a, b):
		sample = []
		for each in self.wordMap[(a,b)]:
			for j in range(self.wordMap[(a,b)][each]):
				sample.append(each)
		return choice(sample)


