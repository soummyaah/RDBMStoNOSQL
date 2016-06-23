"""
@author: Rishikesh
Description: Simple way to convert JSON to xml in python using url request
"""

import requests  # pip install requests
import json
import dicttoxml #pip install dicttoxml
obj = requests.get('https://github.com/timeline.json').json()
xml = dicttoxml.dicttoxml(obj)
print(xml)