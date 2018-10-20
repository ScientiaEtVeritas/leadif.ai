import re
from bs4 import BeautifulSoup
from os import listdir, path
from os.path import isfile, isdir, join

class ReadHTMLFiles:
    def __init__(self, directory):
      self.directory = directory

    def getText(self, page):
        path = '{0}/{1}/www.{1}.de.html'.format(self.directory, page)
        if not isfile(path):
          return print('File does not exist')

        try: 
          file = open(path, "r")
          html = file.read()[3:-1]
        except Exception:
          print('Could not parse file')

        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().replace('\\n', ' ').replace('\\r', '').replace('\\t', '')

        return re.sub( '\s+', ' ', text )

    def getTextOfAllMainPages(self):
      folders = [f for f in listdir(self.directory) if isdir(join(self.directory, f))]
      values = []
      for page in folders:
        values.append({'page': page, 'text': self.getText(page)})
      return values

rd = ReadHTMLFiles('UrlCrawler/output/')
print(rd.getTextOfAllMainPages())