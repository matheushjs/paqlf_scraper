from urllib.request import *
from urllib.parse import *

lookup = input("Romaji word to lookup: ")

url1 = "http://nihongo.monash.edu/cgi-bin/wwwjdic?1E"

values = {
    'dsrchkey': lookup,
    'dicsel': 1,
    'dsrchtype': 'J'}

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

data = urlencode(values)
data = data.encode('utf-8')

request = Request(url1, data, headers=headers)

with urlopen(request) as response:

    print(response.getcode())
    print(response.info())
    print(response.geturl())
    print(response.read().decode('utf-8'))