"""
@author: Rishikesh
Description: Simple way to convert JSON to xml in python using url request
"""

import requests  # pip install requests only for web request 
import json
import dicttoxml # pip install dicttoxml for convert python dictionary to xml
obj = requests.get('https://github.com/timeline.json').json()
xml = dicttoxml.dicttoxml(obj)
print(xml)

# For reverse process XML to JSON 
import xmltodict  # pip install xmltodict

obj = xmltodict.parse("<note><to>Tove</to><from>Jani</from><heading>Reminder</heading><body>Don't forget me this weekend!</body></note>")
json.dumps(obj)   # We can directly convert python dict to json 
