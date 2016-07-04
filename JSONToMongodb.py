"""
@author: Soumya Sharma
Input: databasename
Output: Inserts all json files associated with the databasename to Mongo
Path in line 23 needs to be modified to be used
"""

from pymongo import MongoClient
import sys
import os

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

client = MongoClient('localhost', 27017)

for i in files:
    fileName = i.split("|")[1]
    r = MongoClient('mongoimport --db dbName --collection fileName --file i --jsonArray')

