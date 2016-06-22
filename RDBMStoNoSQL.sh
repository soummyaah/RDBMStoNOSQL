#!/bin/bash

echo "Enter RDBMS: "
read RDBMS
echo "Enter Username: "
read Username
echo "Enter Password: "
read Password
echo "Enter DatabaseName"
read DatabaseName
echo "Enter noSQL: "
read noSQL


if [ "$RDBMS" = "oracle" ]; then
    python ./OracleToJSON.py $Username $Password $DatabaseName
elif [ "$RDBMS" = "mysql" ]; then
    python ./MySQLtoJSON.py $Username $Password $DatabaseName
else
    echo "Error"
fi

if [ "$noSQL" = "elastic" ]; then
    python ./putToElastic.py $DatabaseName
elif [ "$noSQL" = "mongodb" ]; then
    python ./JSONToMongodb.py $DatabaseName
else
    echo "Error"
fi
