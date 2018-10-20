import requests
from bs4 import BeautifulSoup

import asyncio
from aiohttp import ClientSession

class UrlCrawler():
    def getURL(self, page):
        """

        :param page: html of web page (here: Python home page)
        :return: urls in that page
        """
        start_link = page.find("a href")
        if start_link == -1:
            return None, 0
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1: end_quote]
        return url, end_quote

    def findUrls(self, htmlContent):
        page = str(BeautifulSoup(htmlContent, features="lxml"))

        urls = []
        while True:
            url, n = self.getURL(page)
            page = page[n:]
            if url:
                urls.append(url)
            else:
                return urls