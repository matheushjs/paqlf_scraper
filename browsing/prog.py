#Used to make requests
from urllib.request import urlopen, build_opener, install_opener, Request, OpenerDirector, HTTPCookieProcessor
from urllib.parse import urlencode
import os

login_url = "https://secure.runescape.com/m=weblogin/a=13/login.ws"

username = input("Username: ")
password = input("Password: ")

values = {'username': username,
        'password': password,
        'mod': 'www',
        'ssl': 0,
        'dest': 'community?set_lang=0'}

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

data = urlencode(values)
data = data.encode('utf-8')

cookie_proc = HTTPCookieProcessor()
opener = build_opener(cookie_proc)
install_opener(opener)

request = Request(login_url, data, headers=headers)
with urlopen(request) as response:
    print(response.geturl())
    full = response.read().decode('latin1')

import re
patt = re.compile(r'http://services\.runescape\.com/m=forum/a=13/c=[^/]*/forums\.ws\?jptg=ia\&amp;jptv=navbar')
mat = re.findall(patt, full)
fetch_url = mat[0]
print(fetch_url)

request = Request(fetch_url, headers=headers)
with urlopen(request) as response:
    print(response.getcode())
    print(response.info())
    print(response.geturl())
    stream = response.read().decode('latin1')
    #print(cookie_proc.cookiejar.make_cookies(response, request))

    with open('output.html', 'w') as fp:
        fp.write(stream)
