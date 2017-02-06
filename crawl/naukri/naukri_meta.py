# coding=utf-8
import requests
from bs4 import BeautifulSoup
from lib.config_handler import handler
from lib.database import *
import math
import re
import time
class meta():

    def __init__(self):
        self.db = handler('database', 'dbname')
        self.col = handler('database','meta')
        self.obj = operations()

    def crawler(self,url):
        #try:
        page = requests.get(url)
        return page

    #main th for naukri meta 2 phase
    def n_call(self,url):
        page = self.crawler(url)
        obj = operations
        data_arr = self.link_finder(page)
        for data in data_arr:
            self.obj.insert_to_mongo(self.db,self.col,data)
        #print operations.
        self.meta_updater()

    def soup(self,page):
        soup = BeautifulSoup(page.content,"lxml")
        return soup

    def link_finder(self,page):
        data_arr = []
        web_contain = self.soup(page)
        for industry in web_contain.find_all(attrs={"class": "browseIndustry section_white_title"}):
            for jobs in industry.find_all(attrs={"class": "colspan_four collapse"}):
                for list_job in jobs.find_all("a"):
                   data_h = dict()
                   data_h['industry'] = list_job.text
                   data_h['link'] =list_job.get("href").split('?')[0]
                   data_h['source'] = 'naukri'
                   data_h['flag'] = 0
                   data_arr.append(data_h)
        return data_arr

    def meta_updater(self):
        self.finder = self.obj.find_to_mongo(self.db,self.col,{'source':'naukri'})
        try:
            for data in self.finder:
                page = self.crawler(data['link'])
                soup = self.soup(page)
                page_no = self.page_nev(soup)
                data['page_no'] = page_no
                data['industry'] = self.cleaner(data['industry'])
                data['flag'] = 1
                self.obj.update_to_mongo(self.db,self.col,{'link':data['link']},data)
        except:
            print "that link was not processed"

    # find out number of pages on the webiste
    def page_nev(self, soup):
        for count in soup.find_all(attrs={"class": "cnt"}):
            data = self.cleaner(count.text)
            if data is not None and len(data) > 0:
                count = self.cleaner(data.split("of")[1])
                if re.search('(\d)', count):
                    count = float(count)
                    dt = count / float(50)
                    return int(math.ceil(dt))

    def cleaner(self, str):
        strng = ''
        if type(str) != type(""):
            str = str.encode(encoding='UTF-8', errors='strict')
        str = re.sub('[^a-zA-Z0-9-_*.]', ' ', str)
        str = re.sub('[ áá âââââââââââââ¯âãï»¿]+', ' ', str)
        for word in str.split(" "):
            strng += "%s " % (word.strip())
        return strng.strip().lower()


obj = meta()
print "Process start at"
print time.time()
obj.n_call('https://www.naukri.com/jobs-by-category')
print "Prcess ends at"
print time.time()
