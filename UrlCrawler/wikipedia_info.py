import wikipedia
import requests
import urllib
import json
import re

class Wikipedia:
    def __init__(self, hostname):
        self.hostname = hostname
        wikipedia.set_lang('de')

    def getNextItem(self, arr, index):
        try:
            return wikipedia.page(arr[index])
        except Exception:
            if index + 1 < len(arr):
                return self.getNextItem(arr, index + 1)
            else:
                return wikipedia.page(self.hostname)

    def getInfoBoxUrl(self):
        tryout = wikipedia.search(self.hostname)
        if len(tryout) < 1:
            return None
        if len(tryout) >= 1:
            self.search = self.getNextItem(tryout, 0)
            return 'https://de.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xmlfm&titles={0}&rvsection=0'.format(self.search.title)

    def getInfoBoxAsText(self):
        url = self.getInfoBoxUrl()
        if url is None:
            return None
        r = requests.get(url)

        info = re.sub(r'{\{.*\}\}', '', r.text)

        start = info.find('{{Info')

        eof = len(info)

        substring = info[start:eof]

        end = substring.find('}}')

        return info[start:start+end]

    def formatInfoText(self, string):
       string = re.sub(r'(?i)\[\[.*\|','', string).replace(']]','').replace('[[','').replace('\n*',',')
       string = re.sub(r'\<span.*</span>','', string)
       string = string.replace('Website','Homepage')
       string = string.replace('Webseite','Homepage')
       return string.split('\n|')

    def clean_html(self, raw):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw)
        return cleantext

    def getInfoBoxAsDict(self):
       content = self.getInfoBoxAsText()
       if content is None:
           return {}

       result = {}

       content = self.formatInfoText(content)

       for line in content:
           tupel = self.clean_html(line).split('=')
           if(len(tupel)>1):
             if(len(tupel[1].strip())>0):
               result[tupel[0].strip()] = tupel[1].strip()
               result['content'] = self.search.content

       return result

def get_hostname(url):
    return url.split('.')[1]

def isSatisfingSolution(dictionary, key, hostname):
   if key in dictionary:
       if dictionary[key].find(hostname) >-1:
           return True
   return False

def test_with_data(array):
    count = 0
    count_success = 0
    for url in array:
        hostname = get_hostname(url)
        count += 1
        wiki = Wikipedia(hostname)
        dicti = wiki.getInfoBoxAsDict()
        if not isSatisfingSolution(dicti, 'Homepage', hostname):
           wiki = Wikipedia(hostname)
           dicti = wiki.getInfoBoxAsDict()
        if not isSatisfingSolution(dicti, 'Homepage', hostname):
           wiki = Wikipedia(hostname.replace("-",' '))
           dicti = wiki.getInfoBoxAsDict()

        # print(dicti)
        if 'Homepage' in dicti:
            if dicti['Homepage'].find(hostname) >-1:
                count_success += 1
                print ('Hooray ' + dicti['Homepage'] + ' ' + str(round(count_success/count, 2)))
                obj = {'url': url, 'wikipedia': dicti}

                with open('wikipedia.json', 'a') as result_file:
                    result_file.write(json.dumps(obj))

file = open('data.json').read()
array = json.loads(file)

test_with_data(array)