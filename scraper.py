import requests, sys, webbrowser, bs4, urllib2, re, time, datetime, os, ast, nltk
key = "28789a35ac0661133d6500e1e93e0ae24db22fcc"
scores = {}
os.chdir("/Users/devin/Desktop/coding/Python/web_searcher")

def readResults():
	f = open("WOTscores.txt", "r")
	dateModified = time.ctime(os.stat("WOTscores.txt").st_mtime).split(" ")
	dateModifiedStr = "" + dateModified[1] + " " + dateModified[2].zfill(2) + " " + dateModified[4]
	if(str(datetime.datetime.strptime(dateModifiedStr, "%b %d %Y")).split(" ")[0] == str(datetime.date.today())):
		scores = ast.literal_eval(f.readline().strip())
	else:
		scores = {}

def saveResults():
	f = open("WOTscores.txt", "w")
	f.write(str(scores))
	f.close()

def getWOTscore(urlOfSite):
	if(str(urlOfSite) in scores):
		return scores[urlOfSite]
	url = "https://api.mywot.com/0.4/public_link_json?hosts="
	url += urlOfSite + "/&callback=process&key=" + key
	WOTsite = urllib2.urlopen(url)
	WOTdata = WOTsite.read()
	if(WOTdata.count("[") == 4):
		numbers = re.findall("\[.*?\]", WOTdata)
		scores[str(urlOfSite)] = [re.sub("\[|\s|\]", "", numbers[0]).split(","), re.sub("\[|\s|\]", "", numbers[3]).split(",")]
		return [re.sub("\[|\s|\]", "", numbers[0]).split(","), re.sub("\[|\s|\]", "", numbers[3]).split(",")]
	else:
		scores[urlOfSite] = None
		return None

def isSafe(urlOfSite):
	data = getWOTscore(urlOfSite)
	if(data != None and int(data[0][1]) > 10 and int(data[0][0]) > 80 and int(data[1][1]) > 10 and int(data[1][0]) > 80):
		return True
	else:
		return False



def getSearchResults(lookForThis):
	readResults()
	site = urllib2.urlopen('http://duckduckgo.com/html/?q=whatis' + lookForThis)
	data = site.read()
	parsed = bs4.BeautifulSoup(data, "html.parser")
	returnMe = []
	for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
		url = i.a['href']
		url = url[url.find("www.")+4:]
		url = url[:url.find("/")]
		if(isSafe(url)):
			returnMe += [i.a['href']]
	return returnMe
	saveResults()

def getMatchingSentances(url, keyWord):
	try:
		site = urllib2.urlopen(url)
		data = site.read()
		parsed = bs4.BeautifulSoup(data, "html.parser")
		pattern = '(' + keyWord + 's?\s.*?\.)'
		return re.findall(pattern, data)
	except:
		return None

def findGoodSentances(keyWord):
	sitesToSearch = getSearchResults(keyWord)
	for site in sitesToSearch:
		allSentances = getMatchingSentances(site, keyWord)
		if(not allSentances == None):
			for sentance in allSentances:
				sentance = re.sub("[^a-zA-Z\.0-9\s]", "", sentance)
				sentance = nltk.pos_tag(nltk.word_tokenize(sentance))
				if("VB" in sentance[[y[0] for y in sentance].index(keyWord)+1][1]):
					print " ".join([y[0] for y in sentance]) + "---" + site
					os.system("say " + " ".join([y[0] for y in sentance]))


findGoodSentances("Coral")




