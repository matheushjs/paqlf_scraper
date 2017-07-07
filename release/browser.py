from requests import Session
import os
import sys

from processor import Processor, Webpage

class NetworkError(Exception):
    """Convenient exception to show when there is no internet connection"""
    def __init__(self):
        super().__init__(self)

class AuthError(Exception):
    """Convenient exception to show when the user/pass authentication was wrong"""
    def __init__(self):
        super().__init__(self)

class Browser:
    """Class for browing around the Allims website"""

    init_url = "http://administrador.paqlf.allims.com.br/"
    login_url = "http://administrador.paqlf.allims.com.br/controller/login_controle.php"
    home_url = 'http://administrador.paqlf.allims.com.br/laboratorio'

    def __init__(self):
        self.values = {
                'email': "",
                'senha': "" }
        
        self.headers = {}
        self.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        self.headers['X-Requested-With'] = 'XMLHttpRequest'

        self.session = Session()
        self.session.get(Browser.init_url, headers=self.headers)

        self.urldict = {}
    
    def logIn(self, user, pwd):
        """Attempts to log in Allims website.
        Exceptions:
            NetworkError: if there is no network connection
            AuthError: if user/pass combination is wrong"""
        self.values['email'] = user
        self.values['senha'] = pwd
        self.values['acao'] = 'logar'

        try:
            res = self.session.post(Browser.login_url, headers=self.headers, data=self.values)
            res = self.session.get(Browser.home_url, headers=self.headers)
        except:
            raise NetworkError()

        # The log in failure detection condition will consider whether we managed to reach home_url or not
        if res.url != Browser.home_url:
            raise AuthError()

    def countWork(self):
        """Fetches all webpages that need to be processed, and return the amount fetched.
        Exceptions:
            NetworkError: if there is no network connection"""
        self.urldict = {} # Reset the variable
        
        # There should be 4 root pages
        # Each root page has a bunch of pages that lead to samples spreadsheets
        # We have to add the URL for these samples spreadsheets to a list

        # Return the amount of webpages in the list
        return sum( [ len(i) for i in self.urldict.values() ] )

    def processPages(self, dirpath):
        """Processes all the pages fetched with the countWork() method.
        Saves all results into the directory described by 'dirpath'.
        Directories inside the given directory might be created.
        Exceptions:
            NetworkError: if there is no network connection"""
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
