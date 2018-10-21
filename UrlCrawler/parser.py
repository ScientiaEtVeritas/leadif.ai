import requests
import re
from bs4 import BeautifulSoup

class ParseWebsite:
    def __init__(self, url):
        if url.find('://') is not -1:
            self.url = url
        self.url = 'http://' + url

        self.get_HTML()

    def get_HTML(self):
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
    
    def get_all_links(self):
        urls = []
        for a in self.soup.find_all('a', href=True):
            urls.append(a['href'])
        return urls

    def get_social_media_links(self):
        links = self.get_all_links()
        res = {}
        for link in links:
          if link.find('xing') > -1:
            res['xing'] = link
          elif link.find('linkedin') > -1:
            res['linkedin'] = link
          elif link.find('twitter') > -1:
            res['twitter'] = link
          elif link.find('facebook') > -1:
            res['facebook'] = link
        return res
    
    def get_text(self):
        text = self.soup.get_text().replace('\\n', ' ').replace('\\r', '').replace('\\t', '')
        return re.sub( '\s+', ' ', text )

pp = ParseWebsite('www.nordzucker.de')
print(pp.get_social_media_links())
print(pp.get_text())