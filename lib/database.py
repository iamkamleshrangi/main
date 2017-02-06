import pymongo
from config_handler import handler
from pymongo import MongoClient
class operations():
    def __init__(self):
        print 'hello'
        host = handler('database','host')
        port = handler('database','port')
        self.conn = MongoClient(host, port)

    def insert_to_mongo(self,dbname,colname, data):
        db = self.conn[dbname]
        col = db[colname]
        col.insert(data)

    def insert_one(self,dbname,colname,data):
        try:
            db = self.conn[dbname]
            col = db[colname]
            col.insert(data)
            return 1
        except:
            return 0

    def bulk_insert(self,dbname,colname,data_array):
        db = self.conn[dbname]
        col = db[colname]
        col.insert_many(data_array)

    def find_to_mongo(self,dbname,colname,condition):
        try:
            db = self.conn[dbname]
            col = db[colname]
            return col.find(condition)
        except:
            return 0

    def update_to_mongo(self,dbname,colname,condition,data):
        try:
            db = self.conn[dbname]
            col = db[colname]
            col.update(condition,{"$set":data})
            return 1
        except:
            return 0

