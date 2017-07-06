from requests import Session

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

    def __del__(self):
        self.session.close()


if __name__ == "__main__":
    br = Browser()
    try:
        br.logIn('admin', 'admin')
    except NetworkError:
        print("Not connected to the internet!")
    except AuthError:
        print("Invalid log in!")
