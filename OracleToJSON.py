import cx_Oracle
import json

# import MySQLdb
import json
import collections
import sys
from datetime import datetime

if len(sys.argv)!=6:
    print("Correct usage: ./OracleToJSON.py <url:port> <user> <password> <dbName> <tableName>")
    sys.exit()
# 'axia2/axia2@10.1.50.79:1521/ndaie2'
url = sys.argv[1] # url:port
user = sys.argv[2]
password = sys.argv[3]
dbName = sys.argv[4]
tableName = sys.argv[5]
connectionURL = user + "/" + password + "@" + url + "/" + dbName
print(connectionURL)
con = cx_Oracle.connect(connectionURL)
print(con.version)
cursor = con.cursor()

# cursor.execute("SELECT * FROM dba_users")
# print cursor.fetchall()

# query = "USE "
# query += dbName
# cursor.execute(query)

# cursor.execute("select * from tab")
# tables = cursor.fetchall()

# tableList = {}
# for table in tables:
    # tableList[table[0]] = 0
# print(tableList)


# http://stackoverflow.com/questions/8739203/oracle-query-to-fetch-column-names
query = "SELECT COLUMN_NAME FROM cols WHERE TABLE_NAME = \'" 	# Risk from SQL Injection
query += tableName
query += "'"
cursor.execute(query)

columns = [column[0] for column in cursor.fetchall()]

# print(columns)

query = "SELECT * FROM "
query += tableName
cursor.execute(query)

rows = cursor.fetchall()
# print(rows)
rowarray_list = []
for row in rows:
	t = []
	for i in range(len(columns)):
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

objects_list = []
for row in rows:
	d = collections.OrderedDict()
	for i in range(len(columns)):
		try:
			trial = json.dumps(row[i])
			d[columns[i]] = row[i]
		except TypeError:
			d[columns[i]] = str(row[i])
		else:
			pass
	objects_list.append(d)

j = json.dumps(objects_list)

query = "SELECT cols.table_name, cols.column_name, cols.position, cons.status, cons.owner FROM all_constraints cons, all_cons_columns cols WHERE cols.table_name = '"
query += tableName
query += "' AND cons.constraint_type = 'P' AND cons.constraint_name = cols.constraint_name AND cons.owner = cols.owner ORDER BY cols.table_name, cols.position"
cursor.execute(query)
primaryKey = cursor.fetchall()[0][1]       # Assumes only one PK

objects_file = dbName + "-" + tableName + "-" + primaryKey + ".json" 
f = open(objects_file,'w')

print(j, end="", file=f)
print("Yay")

con.close()
