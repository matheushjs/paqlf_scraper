with open('input.html') as fp:
    full = fp.read()

import re

test = 'http://services.runescape.com/m=forum/a=13/c=GNgDP8ssBF0/forums.ws?jptg=ia&jptv=navbar'
patt = re.compile(r'http://services\.runescape\.com/m=forum/a=13/c=[^/]*/forums\.ws\?jptg=ia\&jptv=navbar')
mat = re.match(patt, test)

print(test[mat.start():mat.end()])
