from bs4 import BeautifulSoup
import csv

class Webpage:
    """Class used for representing a named webpage.
    Each webpage has a URL and a name.
    The name is supposed to be used for making a filename to which the results of this webpage's processing will be saved."""
    def __init__(self):
        self.name
        self.url

class Processor:
    """Class used for processing webpages"""
    def __init__(self):
        pass

    def extractSpreadsheet(self, htmlpage, outpath):
        """htmlpage - a string or byte-like variable containing the contents of the webpage to be processed.
        The webpage should be the one containing the spreadsheet with information about each examined sample.
        outpath - the full path of the file to which to save the results of the processing"""
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

    def extractPages(self, url):
        """url - url of the page containing a list of laboratories, each of which link to another page containing its examined samples.
        This method will return a list of Webpage objects, each containing the URL of pages with examined samples, and each having a descriptive name of which laboratory these samples are related to"""
        pages = []
        # Should return a list of WebPages
        return pages
