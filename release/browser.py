from requests import Session
import os
import sys

from processor import *

class NetworkError(Exception):
    """Convenient exception to show when there is no internet connection"""
    def __init__(self, error="Erro na conexão com a internet"):
        self.error = error
        super().__init__(self, error)

    def __str__(self):
        return self.error

class AuthError(Exception):
    """Convenient exception to show when the user/pass authentication was wrong"""
    def __init__(self, error="Erro de autenticação"):
        self.error = error
        super().__init__(self, error)

    def __str__(self):
        return self.error

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

        self.webpages = []
    
    def logIn(self, user, pwd):
        """Attempts to log in Allims website.
        Exceptions:
            NetworkError: if there is no network connection
            AuthError: if user/pass combination is wrong"""
        self.values['email'] = user
        self.values['senha'] = pwd
        self.values['acao'] = 'logar'

        try:
            res = self.session.get(Browser.init_url, headers=self.headers)
            res = self.session.post(Browser.login_url, headers=self.headers, data=self.values)
            res = self.session.get(Browser.home_url, headers=self.headers)
        except:
            raise NetworkError()

        # The log in failure detection condition will consider whether we managed to reach home_url or not
        if res.url != Browser.home_url:
            raise AuthError()

    def countWork(self):
        """Fetches all webpages that need to be processed, and return them.
        Exceptions:
            NetworkError: if there is no network connection
            Exception: if BeautifulSoup fails to parse the response html"""

        try:
            res = self.session.get(Browser.home_url, headers=self.headers)
        except:
            raise NetworkError()

        proc = Processor()

        try:
            self.webpages = proc.extractPages(res.text)
        except:
            raise Exception("Não foi possível processar a página recebida.")

        return self.webpages

    def processPages(self, page, dirpath):
        """Processes all the pages fetched with the countWork() method.
        Saves all results into the directory described by 'dirpath'.
        Directories inside the given directory might be created.
        Exceptions:
            NetworkError: if there is no network connection
            Exception: if BeautifulSoup fails to parse the response html"""
        proc = Processor()
        outfile = os.path.join(dirpath, page.name + ".csv")

        # Make a GET request for the webpage
        try:
            res = self.session.get(page.url, headers=self.headers)
        except:
            raise NetworkError()
        
        try:
            proc.extractSpreadsheet(res.text, outfile)
        except:
            raise Exception("Não foi possível processar a página recebida.")

    def __del__(self):
        try:
            self.session.close()
        except:
            pass

if __name__ == "__main__":
    br = Browser()
    try:
        br.logIn('admin', 'admin')
        print(br.countWork())
    except NetworkError:
        print("Not connected to the internet!")
    except AuthError:
        print("Invalid log in!")
