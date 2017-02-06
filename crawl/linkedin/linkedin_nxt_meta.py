# coding=utf-8
from lib.common import common_methods
from bs4 import BeautifulSoup
from lib.config_handler import handler
from bs4 import Comment
from bs4 import BeautifulSoup as BS
import json
import ast
import re
from lib.database import operations
import urllib
import requests
import time
class execute_meta():
    def __init__(self):
        self.obj = common_methods()
        self.dbcol = operations()
        self.db = handler('database','dbname')
        self.col = handler('database','meta')
        self.agent = requests

    def executor(self):
        linkedin_data = self.dbcol.find_to_mongo(self.db,self.col,{'flag':0})
        try:
            for data in linkedin_data:
                print data
                link = data['link']
                industry = data['industry']
                page = self.agent.get(link).content
                soup = BeautifulSoup(page, "lxml")
                processed_data = self.linkedin_processor(soup)
                time.sleep(5)
        except:
            pass

    #navigation is not working on website
    # to process the linkedin website
    def linkedin_processor(self, soup):
        for jobs in soup.find_all(attrs={"id": "decoratedJobPostingsModule"}):
            job_data = str(jobs).replace('<code id="decoratedJobPostingsModule"><!--', "").replace('--></code>','').replace('\"isInApply":true")', '')
            data_h = ast.literal_eval(json.dumps(job_data).encode('utf8').replace("'", "\""))
            setter = urllib.unquote(data_h)
            pythonDict = json.loads(setter)
            for jobs in pythonDict['paging']['pages']:
                jobs['pageUrl'] = "https://www.linkedin.com%s" % (jobs['pageUrl'])
                jobs['source'] = 'linkedin'
                jobs['flag'] = 2
                print jobs
                self.dbcol.insert_to_mongo(self.db, self.col, jobs)
                print 'inserted'
object = execute_meta()
object.executor()
