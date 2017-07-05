
# coding: utf-8

# In[7]:

from bs4 import BeautifulSoup


# In[42]:

with open('page.html') as fp:
    html_doc = fp.read()

html_doc


# In[43]:

soup = BeautifulSoup(html_doc)

print(soup.prettify())


# In[49]:

print(soup.thead.prettify())


# In[64]:

soup.thead.find_all('td')


# In[88]:

# This snippet fetches all headers from the given HTML
headers = []

for tx in soup.thead.find_all('td'):
    try:
        headers.append([str(tx.b.contents[0].strip()), str(tx.contents[0].contents[1]).strip()])
    except IndexError:
        # First row has only 1 content
        headers.append([str(tx.b.contents[0]).strip()])
    
print(headers)


# In[109]:

# This snippet fetches the contents of the table

content = []

for tx in soup.tbody.find_all('tr'):
    content.append([txx.string for txx in tx.find_all('td')])

for row in content:
    print(row)        


# In[108]:

# This snipped saves the fetched results in a CSV file.

import csv

with open('output.csv', 'w') as fp:
    writer = csv.writer(fp)
    writer.writerow(["\n".join(i) for i in headers])
    writer.writerows(content)


# In[ ]:



