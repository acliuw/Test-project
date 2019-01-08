import http.server
import json
import simplejson
import urllib
from chatbot import *


class Handler(http.server.BaseHTTPRequestHandler):
	def do_POST(self):
		print("Received POST Request")

		print("Length: ", int(self.headers['Content-Length']))
		self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
		self.data_string = urllib.parse.unquote(self.data_string)[8:]
		data = json.loads(self.data_string)

		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		ghbot.update(data)
		ghbot.react(data)




ghbot = GHBot("IAmGithubBot")

server = http.server.HTTPServer(('', 8080), Handler)
server.serve_forever()
