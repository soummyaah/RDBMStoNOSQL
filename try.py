select owner,constraint_name,constraint_type,table_name,r_owner,r_constraint_name from all_constraints where constraint_type='R' and r_constraint_name in (select constraint_name from all_constraints where constraint_type in ('P','U') and table_name='APPLICATION');


"select table_name, constraint_name, status, owner from all_constraints and constraint_type = 'R' and r_constraint_name in ( select constraint_name from all_constraints where constraint_type in ('P', 'U') and table_name = :'APPLICATION') order by table_name, constraint_name"


cursor.execute("select table_name, constraint_name, status, owner from all_constraints where constraint_type = 'R' and r_constraint_name in ( select constraint_name,  from all_constraints where constraint_type in ('P', 'U') and table_name = 'APPLICATION') order by table_name, constraint_name")


SELECT a.table_name, a.column_name, a.constraint_name, c.owner, c.r_owner, c_pk.table_name r_table_name, c_pk.constraint_name r_pk FROM all_cons_columns a JOIN all_constraints c ON a.owner = c.owner AND a.constraint_name = c.constraint_name JOIN all_constraints c_pk ON c.r_owner = c_pk.owner AND c.r_constraint_name = c_pk.constraint_name WHERE c.constraint_type = 'R' AND a.table_name = 'APPLICATION'


select d.table_name, d.constraint_name "Primary Constraint Name", b.constraint_name "Referenced Constraint Name" from user_constraints d, (select c.constraint_name, c.r_constraint_name, c.table_name from user_constraints c  where table_name='APPLICATION' and constraint_type='R') b where d.constraint_name=b.r_constraint_name



SELECT A.COLUMN_NAME, A.TABLE_NAME FROM ALL_CONS_COLUMNS A WHERE A.CONSTRAINT_NAME IN (SELECT CONSTRAINT_NAME FROM ALL_CONSTRAINTS WHERE CONSTRAINT_TYPE='R' AND TABLE_NAME='APPLEGALVEHICLEMAP')



cursor.execute("SELECT * FROM ALL_CONS_COLUMNS WHERE TABLE_NAME='APPLEGALVEHICLEMAP' AND POSITION=1")
a = cursor.fetchall()
relations = [x for x in a if 'FK' in x[1]]

constraintNameToColumnMapper = {}
for i in relations:
	constraintNameToColumnMapper[i[1]] = i[3]

relationResult = []
for i in relations:
	query = "SELECT * FROM ALL_CONSTRAINTS WHERE CONSTRAINT_NAME='"
	cursor.execute(query + i[1] + "'")
	relationResult.append(cursor.fetchall())
	
constraintToConstraintMapper = []
for i in relationResult:
	constraintToConstraintMapper.append([i[0][1],i[0][6]])
	
relationResult = []
for i in constraintNameToColumnMapper:
	query = "SELECT * FROM ALL_CONSTRAINTS WHERE CONSTRAINT_NAME='"
	cursor.execute(query + i[1] + "'")
	relationResult.append(cursor.fetchall())
	
for i in relationResult:
	constraintNameToColumnMapper[i[0][1]] = i[0][3]

	
keys = []
for i in constraintNameToColumnMapper:
	first = constraintNameToColumnMapper[i]
	for i in constraintToConstraintMapper:
		if i[0] == first:
			second = constraintNameToColumnMapper[i[1]]
		if i[1] == first:
			second = constraintNameToColumnMapper[i[0]]
	keys.append(first, second)
	
