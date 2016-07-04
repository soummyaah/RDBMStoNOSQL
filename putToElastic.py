"""
@author: Soumya Sharma
Input: databasename
Output: Inserts all json files associated with the databasename to the elastic search DB
Path in line 24 needs to be modified to be used
"""


import json
import sys
import os
import ast
import pycurl
import StringIO
from elasticsearch import Elasticsearch

if len(sys.argv)!=2:
    print "Correct usage: .\HandlingForeignKeys.py <dbName>"
    sys.exit()

dbName = sys.argv[1]

path = '/media/soumya/New Volume/Nucleus/'
files = {}
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and dbName in i:
        addr = path+i
        files[addr] = ()
# print files
# print
# print
for fileName in files:
    f = open(fileName, 'rb')
    objects = f.readline()  #JSON response printed in one line
    f.close()
    try:
        objects = ast.literal_eval(objects)
    except Exception, e:
        raise e
    files[fileName] = objects

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

for i in files:
    # print
    # print
    response = StringIO.StringIO()
    c = pycurl.Curl()
    fileName = i.split("|")[1]
    # print "fileName: ", fileName
    PK = i.split("|")[2].split(".json")[0]
    # print "PK " + PK
    for j in files[i]:
        _id = j.get(PK)
        # print "id " + str(_id)
        es.index(index=dbName, doc_type=fileName, id=_id, body = j)
