import csv
from urlcrawler import UrlCrawler

INPUT_FILE_PATH = "/home/daniel/Downloads/daten/DEEPTECH-AI Hackathon Daten Uniserv/20181018 Domain+WZ2008 Hackathon INOBAS.csv"

def readUrlsFromInput():
    urls = []
    with open(INPUT_FILE_PATH, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            urls.append(row[0])

    urls.pop(0)
    return urls

urlCrawler = UrlCrawler()
urls = readUrlsFromInput()

for url in urlCrawler.findUrls("http://" + urls[0]):
    print(url)