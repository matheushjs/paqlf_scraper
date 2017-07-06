from requests import Session
import os

from processor import Processor, Webpage

class NetworkError(Exception):
    def __init__(self):
        super().__init__(self)

class AuthError(Exception):
    def __init__(self):
        super().__init__(self)

class Browser:
    login_url = "http://administrador.paqlf.allims.com.br/"

    def __init__(self):
        self.values = {
                'email': "",
                'senha': "" }
        
        self.headers = {}
        self.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

        self.session = Session()

        self.urldict = {}
    
    def logIn(self, user, pwd):
        self.values['email'] = user
        self.values['senha'] = pwd

        try:
            res = self.session.post(Browser.login_url, headers=self.headers, data=self.values)
        except:
            raise NetworkError()

        # The log in failure detection condition will consider if whether we've been redirected or not
        if res.url == Browser.login_url:
            raise AuthError()

    def countWork(self):
        self.urldict = {} # Reset the variable
        
        # There should be 4 root pages
        # Each root page has a bunch of pages that lead to samples spreadsheets
        # We have to add the URL for these samples spreadsheets to a list

        # Return the amount of webpages in the list
        return sum( [ len(i) for i in self.urldict.values() ] )

    def processPages(self, dirpath):
        proc = Processor()

        for key in self.urldict.keys():
            newdir = os.path.join(dirpath, key)
            os.mkdir(newdir)
            
            for webpage in self.urldict[key]:
                # Make the file name
                # outfile = os.path.join(newdir, )
                # process the webpage and save in the file
                outfile = os.path.join(newdir, webpage.name + ".csv")

                # Make a GET request for the webpage
                try:
                    res = self.session.get(webpage.url, headers=self.headers)
                except:
                    raise NetworkError()
                proc.extractSpreadsheet(res.text, outfile)

    def __del__(self):
        self.session.close()


if __name__ == "__main__":
    br = Browser()
    try:
        br.logIn('admin', 'admin')
        print(br.countWork())
    except NetworkError:
        print("Not connected to the internet!")
    except AuthError:
        print("Invalid log in!")
