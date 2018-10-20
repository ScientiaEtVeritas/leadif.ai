import requests
import json

NPUT_FILE_PATH = "./20181018 Domain+WZ2008 Hackathon INOBAS.csv"

def readInputData():
    inputData = []

    with open("./output/output.json", "r") as file:
        inputData = json.loads(file.read())

    return inputData

def getWatsonAnalysis(url):
    url = url.replace("https", "http")
    response = requests.post("https://natural-language-understanding-demo.ng.bluemix.net/api/analyze", json={
		'features': {
			'categories': {},
			'concepts': {},
			'emotion': {},
			'entities':{},
			'keywords': {},
			'semantic_roles': {},
			'sentiment':{}
		},
		'url': url
	})

    if response.status_code != 200: return ""

    print("analysed " + url)
    return response.text

def loadExistingData():
    data = []
    with open("./output/watson.json", "r") as file:
        data = json.loads(file.read())
    return data

def saveWatsonResponse(url, response, existingData):
    existingData.append({
        'url': url,
        'response': response
    })

    with open("./output/watson.json", "w") as file:
        file.write(json.dumps(existingData, indent=4))

def urlExists(url, data):
    for entry in data:
        if entry['url'] == url:
            return True
    return False

existingData = loadExistingData()
inputData = readInputData()
for company in inputData:
    url = company['url']
    if urlExists(url, existingData):
        print(url + " already analysed")
        continue
    try:
        response = json.loads(getWatsonAnalysis(url))
        saveWatsonResponse(url, response, existingData)
    except:
        print("failed to analyse " + url)