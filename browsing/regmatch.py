with open('input.html') as fp:
    full = fp.read()

import re

test = """akjdbwyawjydbajwdawy
http://services.runescape.com/m=forum/a=13/c=GNgDP8ssBF0/forums.ws?jptg=ia&amp;jptv=navbar"""
patt = re.compile(r'http://services\.runescape\.com/m=forum/a=13/c=[^/]*/forums\.ws\?jptg=ia\&amp;jptv=navbar')

mat = re.findall(patt, full)

print(mat)
#print(full[mat.start():mat.end()])
