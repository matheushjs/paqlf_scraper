'''
Created on May 28, 2017

@author: mathjs
'''

import requests

login_url = "https://secure.runescape.com/m=weblogin/a=13/login.ws"

username = input("Username: ")
password = input("Password: ")

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

values = {'username': username,
        'password': password,
        'mod': 'www',
        'ssl': 0,
        'dest': 'community?set_lang=0'}

s = requests.Session()
r = s.post(login_url, headers=headers, data=values)
print(r.url)

import re
patt = re.compile(r'http://services\.runescape\.com/m=forum/a=13/c=[^/]*/forums\.ws\?jptg=ia\&amp;jptv=navbar')
mat = re.findall(patt, r.text)
fetch_url = mat[0]
print(fetch_url)

r = s.get(fetch_url, headers=headers)
print(r.status_code)
print(r.url)

with open('output.html', 'w') as fp:
    fp.write(r.text) # WORKS