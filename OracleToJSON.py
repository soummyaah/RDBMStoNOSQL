import cx_Oracle
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

#To fetch Column Names
query = "SELECT COLUMN_NAME FROM cols WHERE TABLE_NAME = \'" 	# Risk from SQL Injection
query += tableName
query += "'"
cursor.execute(query)

columns = [column[0] for column in cursor.fetchall()]

# To fetch Foreign Keys

cursor.execute("SELECT * FROM ALL_CONS_COLUMNS WHERE TABLE_NAME='" + tableName + "' AND POSITION=1")
a = cursor.fetchall()
relations = [x for x in a if 'FK' in x[1]]

constraintNameToColumnMapper = {}
for i in relations:
	constraintNameToColumnMapper[i[1]] = (i[3], i[2],)

relationResult = []
for i in relations:
	query = "SELECT * FROM ALL_CONSTRAINTS WHERE CONSTRAINT_NAME='"
	cursor.execute(query + i[1] + "'")
	relationResult.append(cursor.fetchall())
	
constraintToConstraintMapper = []
for i in relationResult:
	constraintToConstraintMapper.append([i[0][1],i[0][6]])
	
relationResult = []
for i in constraintToConstraintMapper:
	query = "SELECT * FROM ALL_CONS_COLUMNS WHERE CONSTRAINT_NAME='"
	cursor.execute(query + i[1] + "'")
	relationResult.append(cursor.fetchall())
	
for i in relationResult:
	constraintNameToColumnMapper[i[0][1]] = (i[0][3], i[0][2])

keys = []
for i in constraintToConstraintMapper:
	first = constraintNameToColumnMapper[i[0]]
	second = constraintNameToColumnMapper[i[1]]
	keys.append([first, second])

print("Foreign Keys:","\n")
print("Index [(ColumnName1, TableName1), (ColumnName2, TableName2)]", "\n")
for index, elem in enumerate(keys):
	print(index, elem,"\n")



# Take choice of FK to be included	
print("Include any column as new object within original JSON object?(Y/N):")
choice = input()
includeFK = []
while choice=='y' or choice=='Y' or choice=="yes":
	id = int(input())
	if id >= 0 and id < len(keys):
		includeFK.append(keys[id])
	else:
		print("Invalid id")
	print("Include any other column(Y/N):")
	choice = input()

print(includeFK)
FKColumnName = []
for i in includeFK:
	if tableName==i[0][1]:
		FKColumnName.append(i[0][0])
	else:
		FKColumnName.append(i[1][0])

print(FKColumnName)
# To fetch rows
query = "SELECT * FROM "
query += tableName
cursor.execute(query)

rows = cursor.fetchall()
# print(rows)

print(columns)

# To convert data to a list of json objects
objects_list = []
for row in rows:
	d = collections.OrderedDict()
	for i in range(len(columns)):
		if columns[i] in FKColumnName:
			print(row[i])
			for z in keys:
				if columns[i] == z[0][0] and tableName == z[0][1]:
					FKTableName = z[1][1]
					query = "SELECT * FROM " + FKTableName + " WHERE " + z[1][0] + "=" + str(row[i])
				elif columns[i] == z[1][0] and tableName == z[1][1]:
					FKTableName = z[0][1]
					query = "SELECT * FROM " + FKTableName + " WHERE " + z[0][0] + "=" + str(row[i])
			print(FKTableName)
			print(query)
			cursor.execute(query)
			FKRows = cursor.fetchall()
			print(FKRows)
			FKColumns = []
			query = "SELECT COLUMN_NAME FROM cols WHERE TABLE_NAME = \'" 	# Risk from SQL Injection
			query += FKTableName
			query += "'"
			cursor.execute(query)
			
			FKColumns = [column[0] for column in cursor.fetchall()]
			print(FKColumns)
			fkobjects_list = []
			for fkrow in FKRows:
				q = collections.OrderedDict()
				for z in range(len(FKColumns)):
					try:
						trial = json.dumps(fkrow[z])
						q[FKColumns[z]] = fkrow[z]
					except TypeError:
						d[FKColumns[z]] = str(fkrow[z])
					else:
						pass
				fkobjects_list.append(q)
				d[columns[i]] = fkobjects_list
		else:
			try:
				trial = json.dumps(row[i])
				d[columns[i]] = row[i]
			except TypeError:
				d[columns[i]] = str(row[i])
			else:
				pass
	objects_list.append(d)

j = json.dumps(objects_list)

# To get PrimaryKey column name.
# Assumes only 1 PK exists
query = "SELECT cols.table_name, cols.column_name, cols.position, cons.status, cons.owner FROM all_constraints cons, all_cons_columns cols WHERE cols.table_name = '"
query += tableName
query += "' AND cons.constraint_type = 'P' AND cons.constraint_name = cols.constraint_name AND cons.owner = cols.owner ORDER BY cols.table_name, cols.position"
cursor.execute(query)
primaryKey = cursor.fetchall()[0][1]       # Assumes only one PK

# File Name
objects_file = dbName + "-" + tableName + "-" + primaryKey + ".json" 
f = open(objects_file,'w')

# Printing to file
print(j, end="", file=f)
print("Yay")

con.close()
