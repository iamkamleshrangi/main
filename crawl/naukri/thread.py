# coding=utf-8
import requests
from lib.database import operations
from lib.config_handler import handler
import re
from bs4 import BeautifulSoup
import threading
class Cralwer_thread():
    def __init__(self):
        self.agent = requests
        self.db = handler('database','dbname')
        self.metacol = handler('database','meta')
        self.col = handler('database','process')
        self.opobj = operations()

    def worker(self):
        finder = self.opobj.find_to_mongo(self.db,self.metacol,{'source':'naukri'})
        if len(finder) > 0:
            thread1 = myThread(1, "Thread-1", 1)
