# coding=utf-8
import Queue
import threading
import time
from lib.database import operations
from lib.config_handler import handler
import requests
import time
import re
from bs4 import BeautifulSoup
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            for data in threadName:
                link = data['link']
                industry = data['industry']
                page_no = data['page_no']
                get_page(link, industry, page_no)
                break
        else:
            queueLock.release()
        time.sleep(1)
def get_page(self,link, industry, page_no):
    for page in range(1,int(page_no)+1):
        uri = '%s-%s'%(link,page)
        page = self.agent.get(uri).content
        self.page_processor(page)
        break
def cleaner(str):
    strng = ''
    if type(str) != type(""):
        str = str.encode(encoding='UTF-8', errors='strict')
    str = re.sub('[^a-zA-Z0-9-_*.]', ' ', str)
    str = re.sub('[ áá âââââââââââââ¯âãï»¿]+', ' ', str)
    for word in str.split(" "):
        strng += "%s " % (word.strip())
    return strng.strip().lower()

def page_processor(content):
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
            data_h['job_id'] = cleaner(id)

        if job_link != None and len(job_link) > 2:
            data_h['job_link'] = cleaner(job_link)

        if designation != None and len(designation):
            data_h['designation'] = cleaner(designation)

        if organization != None and len(organization):
            data_h['organization'] = cleaner(organization)

        if experience != None and len(experience):
            data_h['experience'] = cleaner(experience)

        if location != None and len(location):
            data_h['locaton'] = cleaner(location)

        if key_skills != None and len(key_skills):
            data_h['key_skill'] = cleaner(key_skills)

        if salary != None and len(salary):
            data_h['salary'] = cleaner(salary)

        if posted_by != None and len(posted_by):
            data_h['posted_by'] = cleaner(posted_by)
        opobj.insert_to_mongo(db,col,data =data_h)

agent = requests
db = handler('database','dbname')
metacol = handler('database','meta')
col = handler('database','process')
opobj = operations()



threadList = opobj.find_to_mongo(db,metacol,{'source':'naukri'})
nameList = [range(1,threadList.count())]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"