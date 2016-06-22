import cx_Oracle
import json

import MySQLdb
import json
import collections
import sys
from datetime import datetime

if len(sys.argv)!=4:
    print("Correct usage: ./OracleToJSON.py <user> <password> <dbName>")
    sys.exit()

user = sys.argv[1]
password = sys.argv[2]
dbName = sys.argv[3]

axia2@//10.1.50.79:1521/ndaie2

connectionURL = user + "/" + password + "@127.0.0.1/" + dbName
con = cx_Oracle.connect(connectionURL)
print(con.version)
exit(1)
cursor = con.cursor()

# cursor.execute("SHOW DATABASES")
# print cursor.fetchall()

query = "USE "
query += dbName
cursor.execute(query)

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

tableList = {}
for table in tables:
    tableList[table[0]] = 0
print(tableList)

for table in tableList:
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'"
    query += dbName
    query += "\' AND TABLE_NAME = \'"
    query += table
    query += "'"
    cursor.execute(query)

    columns = [column[0] for column in cursor.fetchall()]

    query = "SELECT * FROM "
    query += table
    cursor.execute(query)

    rows = cursor.fetchall()
    print(rows)
    rowarray_list = []
    for row in rows:
        t = []
        for i in xrange(len(columns)):
            try:
                trial = json.dumps(row[i])
                t.append(row[i])
            except TypeError:
                t.append(str(row[i]))
            else:
                pass
        rowarray_list.append(tuple(t))

    print(rowarray_list)
    j = json.dumps(rowarray_list)
    print("Yay")

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        for i in xrange(len(columns)):
            try:
                trial = json.dumps(row[i])
                d[columns[i]] = row[i]
            except TypeError:
                d[columns[i]] = str(row[i])
            else:
                pass
        objects_list.append(d)

    j = json.dumps(objects_list)
    objects_file = dbName + "|" + table + ".json"
    f = open(objects_file,'w')
    cursor.execute("SHOW INDEX FROM " + table)
    primaryKey = cursor.fetchall()[0]       # Assumes only one PK
    print >> f, primaryKey[4]
    print >> f, j

con.close()
