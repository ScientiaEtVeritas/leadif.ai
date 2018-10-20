import csv
from bs4 import BeautifulSoup
import json
import grequests
import re
import os

INPUT_FILE_PATH = "/home/daniel/Downloads/daten/DEEPTECH-AI Hackathon Daten Uniserv/20181018 Domain+WZ2008 Hackathon INOBAS.csv"

def readInputData():
    inputData = []
    with open(INPUT_FILE_PATH, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if not row[0].startswith("http"):
                row[0] = "http://" + row[0]
            inputData.append({
                'url': row[0],
                'WZ2008 Section': row[1],
                'WZ2008 Code': row[2],
                'subpages': []
            })

    inputData.pop(0)
    return inputData

def loadAllSiteContents(urls):
    rs = (grequests.get(u, timeout=0.001) for u in urls)
    responses = grequests.map(rs)
    contents = []
    for response in responses:
        if response is None:
            contents.append("")
        else:
            contents.append(response.content)
    return contents

def findUrlsInSite(htmlContent, mainUrl):
    page = BeautifulSoup(htmlContent, features="lxml")

    urls = []
    for a in page.find_all('a', href=True):
        url = a['href']
        if not url.startswith("http"):
            url = mainUrl + "/" + url
        if not url in urls:
            urls.append(url)

    return urls

def saveHtml(url, html, mainUrl):
    folderName = mainUrl
    try:
        folderName = re.search(r'www\.(.*?)\.de', mainUrl).group(1)
    except:
        pass

    if not os.path.exists("./output/" + folderName):
        os.makedirs("./output/" + folderName)

    filename = url.split('/')[-1]
    if filename == "": filename = url.split('/')[-2]
    with open("./output/" + folderName + "/" + filename + '.html', "w")  as file:
        file.write(str(html))


print("reading input file...")
inputData = readInputData()
inputUrls = [company['url'] for company in inputData]

print("downloading main page contents...")
siteContents = loadAllSiteContents(inputUrls[:10])

print("parsing main page contents...")
i = 0
for siteContent in siteContents:
    saveHtml(inputData[i]['url'], siteContent, inputData[i]['url'])
    inputData[i]['subpages'] = findUrlsInSite(siteContent, inputData[i]['url'])
    i += 1

print("writing output file")
with open("./output/output.json", "w")  as file:
    file.write(json.dumps(inputData, sort_keys=True, indent=4))

print("downloading all subpages...")
subpages = []
for company in inputData:
    subpages.extend(company['subpages'])

companySubPageContents = loadAllSiteContents(subpages)

subpageContentIndex = 0
for company in inputData:
    for subpageUrl in company['subpages']:
        if subpageContentIndex >= len(companySubPageContents): break
        saveHtml(subpageUrl, companySubPageContents[subpageContentIndex], company['url'])
        subpageContentIndex += 1