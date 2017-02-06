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
        self.process = handler('database','process')

    def executor(self):
        linkedin_data = self.dbcol.find_to_mongo(self.db,self.col,{'flag':2})
        for data in linkedin_data:
            link = data['pageUrl']
            page = self.agent.get(link).content
            soup = BeautifulSoup(page, "lxml")
            processed_data = self.linkedin_processor(soup)
            time.sleep(5)

    #navigation is not working on website
    # to process the linkedin website
    def linkedin_processor(self, soup):
        for jobs in soup.find_all(attrs={"id": "decoratedJobPostingsModule"}):
            job_data = str(jobs).replace('<code id="decoratedJobPostingsModule"><!--', "").replace('--></code>','').replace('\"isInApply":true")', '')
            data_h = ast.literal_eval(json.dumps(job_data).encode('utf8').replace("'", "\""))
            setter = urllib.unquote(data_h)
            pythonDict = json.loads(setter)
            for jobs in pythonDict['elements']:
                jobs['source'] = 'linkedin'
                jobs['flag'] = 1
                #print jobs
                self.dbcol.insert_to_mongo(self.db, self.process, jobs)
                #print 'inserted'

object = execute_meta()
object.executor()
