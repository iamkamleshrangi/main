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
class linkedin_meta():

    def __init__(self):
        self.obj = common_methods()
        self.dbcol = operations()
        self.db = handler('database','dbname')
        self.col = handler('database','meta')
        self.agent = requests

    def page(self):
        page = self.obj.get_page('https://www.linkedin.com/jobs').content
        self.get_links(page)

    def get_links(self,page):
        soup = BeautifulSoup(page ,"lxml")
        for job_crads in soup.find_all(attrs={"class":"gjh-card jserp-search-card"}):
            uri ="https://www.linkedin.com/jobs/%s"%(job_crads.find(attrs={"class":"view-all-link"}).get("href"))
            industry = job_crads.text.replace('View all','')
            data_h = dict()
            data_h['link'] = uri
            data_h['industry'] = industry
            data_h['flag']= 0
            data_h['source'] = 'linkedin'
            self.dbcol.insert_to_mongo(self.db, self.col, data_h)

obj = linkedin_meta()
obj.page()