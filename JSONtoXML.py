"""
@author: Rishikesh
Description: Simple way to convert JSON to xml in python using url request
"""

import requests  # pip install requests only for web request 
import json
import dicttoxml #pip install dicttoxml for convert python dictionary to xml
obj = requests.get('https://github.com/timeline.json').json()
xml = dicttoxml.dicttoxml(obj)
print(xml)
