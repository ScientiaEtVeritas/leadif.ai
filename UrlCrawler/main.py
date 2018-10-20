import csv
from bs4 import BeautifulSoup
import json
import grequests
import re
import os
import os.path
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (110000, 110000))

INPUT_FILE_PATH = "./20181018 Domain+WZ2008 Hackathon INOBAS.csv"

def readInputData():
    inputData = []
    with open(INPUT_FILE_PATH, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if not row[0].startswith("http"):
                row[0] = "https://" + row[0]

            if fileForUrlExists(row[0]):
                print("already existing: " + row[0])
                continue

            inputData.append({
                'url': row[0],
                'WZ2008 Section': row[1],
                'WZ2008 Code': row[2],
                'subpages': []
            })

    inputData.pop(0)
    return inputData

def loadAllSiteContents(urls):
    rs = (grequests.get(u, timeout=2) for u in urls)
    responses = grequests.map(rs, size=5)
    contents = []
    for response in responses:
        if response is None:
            contents.append("")
        else:
            contents.append(response.content)
    return contents

def findUrlsInSite(htmlContent, mainUrl):
    page = BeautifulSoup(htmlContent)

    urls = []
    for a in page.find_all('a', href=True):
        url = a['href']
        if not url.startswith("http"):
            url = mainUrl + "/" + url
        if not url in urls and not " " in url:
            urls.append(url.replace(".de//", ".de/"))

    return urls

def fileForUrlExists(url):
    file = "./output/" + getFolderNameForUrl(url) + "/" + getFileNameForUrl(url)
    return os.path.isfile(file) and not os.stat(file).st_size == 0

def getFolderNameForUrl(url):
    folderName = url
    try:
        folderName = re.search(r'www\.(.*?)\.de', url).group(1)
    except:
        pass

    return folderName

def getFileNameForUrl(url):
    filename = url.split('/')[-1]
    if filename == "": filename = url.split('/')[-2]
    return filename + ".html"

def saveHtml(url, html, mainUrl):
    folderName = getFolderNameForUrl(mainUrl)

    if not os.path.exists("./output/" + folderName):
        os.makedirs("./output/" + folderName)

    with open("./output/" + folderName + "/" + getFileNameForUrl(url), "w")  as file:
        html = str(html)
        if html.startswith("b'"):
            html = html[2:]
        file.write(html)


print("reading input file...")
inputData = readInputData()
inputUrls = [company['url'] for company in inputData]

print("downloading main page contents...")
siteContents = loadAllSiteContents(inputUrls)

print("parsing main page contents...")
i = 0
for siteContent in siteContents:
    saveHtml(inputData[i]['url'], siteContent, inputData[i]['url'])
    inputData[i]['subpages'] = findUrlsInSite(siteContent, inputData[i]['url'])
    i += 1

print("writing output file")
with open("./output/output.json", "w")  as file:
    file.write(json.dumps(inputData, sort_keys=True, indent=4))

'''
print("downloading all subpages...")
subpages = []
for company in inputData:
    subpages.extend(company['subpages'])

companySubPageContents = loadAllSiteContents2(subpages)

print("saving all subpages...")
subpageContentIndex = 0
for company in inputData:
    for subpageUrl in company['subpages']:
        if subpageContentIndex >= len(companySubPageContents): break
        saveHtml(subpageUrl, companySubPageContents[subpageContentIndex], company['url'])
        subpageContentIndex += 1
'''