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

    if os.path.isfile("./output/output.json"):
        with open("./output/output.json", "r") as file:
            inputData = json.loads(file.read())

    with open(INPUT_FILE_PATH, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if row[0] == "Domain": continue
            if not row[0].startswith("http"):
                row[0] = "https://" + row[0]

            if urlExistsInData(inputData, row[0]): continue

            inputData.append({
                'url': row[0],
                'WZ2008 Section': row[1],
                'WZ2008 Code': row[2],
                'subpages': [],
                'text': '',
                'image': ''
            })

    return inputData

def urlExistsInData(data, url):
    for company in data:
        if company['url'] == url:
            return True
    return False

def urlIsCompleteInData(data, url):
    if not fileForUrlExists(url): return False
    for company in data:
        if company['url'] == url:
            if "text" in company and company["text"] != "" and len(company['subpages']) != 0:
                return True
    return False

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
        url = url.replace(".de//", ".de/")
        if not url in urls and not " " in url:
            urls.append(url)

    return urls

def getText(content):
    page = BeautifulSoup(content)
    text = page.get_text().replace('\\n', ' ').replace('\\r', '').replace('\\t', '')

    return re.sub( '\s+', ' ', text )

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

def getIndexOfUrl(data, url):
    i = 0
    for company in data:
        if company['url'] == url:
            return i
        i += 1
    return False


print("reading input file...")
inputData = readInputData()
inputUrls = []

#collect all urls which need to be downloaded
for company in inputData:
    if urlIsCompleteInData(inputData, company['url']):
        print("already scrawled: " + company['url'])
        continue
    inputUrls.append(company['url'])

print("downloading main page contents...")
siteContents = loadAllSiteContents(inputUrls)

print("parsing main page contents...")
i = 0
for siteContent in siteContents:
    saveHtml(inputData[getIndexOfUrl(inputData, inputUrls[i])]['url'], siteContent, inputData[getIndexOfUrl(inputData, inputUrls[i])]['url'])
    inputData[getIndexOfUrl(inputData, inputUrls[i])]['subpages'] = findUrlsInSite(siteContent, inputData[getIndexOfUrl(inputData, inputUrls[i])]['url'])
    inputData[getIndexOfUrl(inputData, inputUrls[i])]['text'] = getText(siteContent)

    imagePath = "./screenshots/" + inputData[getIndexOfUrl(inputData, inputUrls[i])]['url'].replace("http://", "").replace("https://", "").replace("/", "") + ".png"
    inputData[getIndexOfUrl(inputData, inputUrls[i])]['image'] = imagePath
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