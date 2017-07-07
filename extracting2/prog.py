
# coding: utf-8

# In[2]:

from bs4 import BeautifulSoup
import csv

with open("home.html") as fp:
    html_doc = fp.read()

html_doc


# In[5]:

soup = BeautifulSoup(html_doc, 'lxml')

print(soup.prettify())


# In[21]:

headers = []

for tx in soup.thead.find_all('td'):
    try:
        headers.append(str(tx.b.string))
    except:
        pass

headers


# In[69]:

for tx in soup.tbody.find_all('tr'):
    conts = tx.contents
    number = conts[1].string
    lab = conts[2].string
    sample_url = conts[11].a['href']
    print(number, lab, sample_url)


# In[ ]:



