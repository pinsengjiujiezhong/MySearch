#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2020/5/2 21:01'

import pymongo,requests,re
from datetime import datetime
from elasticsearch import Elasticsearch

conn = pymongo.MongoClient('127.0.0.1')
mydb = conn.blog
p = mydb.wenzhang
q = mydb.wenzhang1

cursor=q.find()
# for item in cursor:
#     img = item['url']
#     id = img.split('/')[-2]
#     item['id'] = id
#     q.insert(item)

from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="127.0.0.1", port=9200)
es.indices.create(index="kai", ignore=400)

for item in cursor:
    del item['_id']
    res = es.index(index="kai", doc_type="doc", body=item)
