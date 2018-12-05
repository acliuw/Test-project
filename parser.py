import json

reviews = open("textdata/reviews_Video_Games_short_5.json", "r").read().split("\n")

outF = open("textdata/five-star-amazon-video-games.txt","w")

for review in reviews:
	try:
		data = json.loads(review)
	except:
		print("error")
	if data["overall"] == 5 and len(data["reviewText"]) > 5:
		outF.write(data["reviewText"])

		if (data["reviewText"][-1] not in [".","!","?"]):
			outF.write(".")
		outF.write("\n")

outF.close()