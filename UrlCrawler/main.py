import csv
from urlcrawler import UrlCrawler
import json
import grequests

INPUT_FILE_PATH = "/home/daniel/Downloads/daten/DEEPTECH-AI Hackathon Daten Uniserv/20181018 Domain+WZ2008 Hackathon INOBAS.csv"
inputData = []
inputUrls = []

def readUrlsFromInput():
    with open(INPUT_FILE_PATH, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if not row[0].startswith("http"):
                row[0] = "http://" + row[0]
            inputData.append({
                'url': row[0],
                'WZ2008 Section': row[1],
                'WZ2008 Code': row[2]
            })
            inputUrls.append(row[0])

    inputData.pop(0)

def loadAllUrls(urls):
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    contents = []
    for response in responses:
        contents.append(response.content)
    return contents

readUrlsFromInput()
siteContents = loadAllUrls(inputUrls[:5])
urlCrawler = UrlCrawler()

i = 0
for siteContent in siteContents:
    inputData[i]['subpages'] = urlCrawler.findUrls(siteContent)
    print(str(i))
    i += 1

with open("output.json", "w")  as file:
    file.write(json.dumps(inputData, sort_keys=True, indent=4))