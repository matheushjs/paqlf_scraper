from bs4 import BeautifulSoup
import csv

class Processor:
    def __init__(self):
        pass

    def extractSpreadsheet(self, htmlpage, outpath):
        soup = BeautifulSoup(htmlpage)
        
        # Extract headers of the spreadsheet
        headers = []
        for tx in soup.thead.find_all('td'):
            try:
                headers.append([str(tx.b.contents[0].strip()), str(tx.contents[0].contents[1]).strip()])
            except IndexError:
                # First row has only 1 content
                headers.append([str(tx.b.contents[0]).strip()])

        # Extract the spreadsheet's content
        content = []
        for tx in soup.tbody.find_all('tr'):
            content.append([txx.string for txx in tx.find_all('td')])

        # Save spreadsheet to file
        with open(outpath, 'w') as fp:
            writer = csv.writer(fp)
            writer.writerow(["\n".join(i) for i in headers])
            writer.writerows(content)
