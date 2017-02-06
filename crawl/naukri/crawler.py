# coding=utf-8
import requests
from lib.database import operations
from lib.config_handler import handler
import re
from bs4 import BeautifulSoup

class Cralwer():
    def __init__(self):
        self.agent = requests
        self.db = handler('database','dbname')
        self.metacol = handler('database','meta')
        self.col = handler('database','process')
        self.opobj = operations()

    def worker(self):
        finder = self.opobj.find_to_mongo(self.db,self.metacol,{'source':'naukri'})
        for data in finder:
            link = data['link']
            industry = data['industry']
            page_no =  data['page_no']
            self.get_page(link,industry,page_no)
            break

    def get_page(self,link, industry, page_no):
        for page in range(1,int(page_no)+1):
            uri = '%s-%s'%(link,page)
            page = self.agent.get(uri).content
            self.page_processor(page)
            break

    def page_processor(self,content):
        print 'hello content'
        print content
        soup = BeautifulSoup(content,'html.parser')

        for jobs in soup.find_all(attrs={"itemtype":"http://schema.org/JobPosting"}):
            id = jobs.get("id")
            job_link = jobs.get("href")
            designation = jobs.find(attrs={"class":"desig"}).text
            organization = jobs.find(attrs={"class":"org"}).text
            experience = jobs.find(attrs={"class":"exp"}).text
            location = jobs.find(attrs ={"class":"loc"}).text
            key_skills = jobs.find(attrs={"class":"more"}).text
            salary = jobs.find(attrs={"class":"salary"}).text
            posted_by = jobs.find(attrs={"class":"rec_name"}).text

            #data formating
            data_h = dict()
            if id != None and len(id) >2:
                data_h['job_id'] = self.cleaner(id)

            if job_link != None and len(job_link) > 2:
                data_h['job_link'] = self.cleaner(job_link)

            if designation != None and len(designation):
                data_h['designation'] = self.cleaner(designation)

            if organization != None and len(organization):
                data_h['organization'] = self.cleaner(organization)

            if experience != None and len(experience):
                data_h['experience'] = self.cleaner(experience)

            if location != None and len(location):
                data_h['locaton'] = self.cleaner(location)

            if key_skills != None and len(key_skills):
                data_h['key_skill'] = self.cleaner(key_skills)

            if salary != None and len(salary):
                data_h['salary'] = self.cleaner(salary)

            if posted_by != None and len(posted_by):
                data_h['posted_by'] = self.cleaner(posted_by)

            self.opobj.insert_to_mongo(self.db,self.col,data =data_h)

    def cleaner(self, str):
        strng = ''
        if type(str) != type(""):
            str = str.encode(encoding='UTF-8', errors='strict')
        str = re.sub('[^a-zA-Z0-9-_*.]', ' ', str)
        str = re.sub('[ áá âââââââââââââ¯âãï»¿]+', ' ', str)
        for word in str.split(" "):
            strng += "%s " % (word.strip())
        return strng.strip().lower()

obj = Cralwer()
obj.worker()