'''
Created on May 28, 2017

@author: mathjs
'''

import requests

url1 = "http://nihongo.monash.edu/cgi-bin/wwwjdic?1E"
lookup = 'chotto'

r = requests.post(url1, data = {
    'dsrchkey': lookup,
    'dicsel': 1,
    'dsrchtype': 'J'})

print(r.text)
print(r.url)
print(r.headers)