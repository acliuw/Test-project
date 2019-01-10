import re
import json
import nltk
from random import *

text = open("trump-tweets.txt", "r").read()
cleaned = open("trump-tweets-cleaned.txt","w")
data = json.loads(text)

for tweet in data["payload"]:
	cleaned.write(tweet["text"] + "\n")
cleaned.close()
