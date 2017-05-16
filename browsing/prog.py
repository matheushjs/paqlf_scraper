#Used to make requests
import urllib.request

login_url = "https://secure.runescape.com/m=weblogin/loginform.ws?mod=www&ssl=0&dest=community%3Fset_lang%3D0"
fetch_url = "http://services.runescape.com/m=forum/a=13/c=UoOPoqElGmI/forums.ws?259,260,607,62837244"

username = input("Username: ")
password = input("Password: ")

values = {'login-username': username,
        'login-password': password }

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
request = urllib.request.Request(login_url, data, headers=headers)
response = urllib.request.urlopen(request)

print(urllib.request.urlopen(fetch_url).read())
