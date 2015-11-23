# coding=utf-8

import http.cookiejar
import urllib.request
import urllib.parse
import random
import time
import socket


# sys.path.append("F:/myspace/workspace1/ucs_spider/src")


ERROR_CODE_SUCCESS = 0
ERROR_CODE_NOTFOUND = 1
ERROR_CODE_IO = 2
ERROR_CODE_PARSE = 3
ERROR_CODE_DB = 4
ERROR_CODE_INHIBIT = 5
ERROR_CODE_EXPIRED = 6
ERROR_CODE_ENCODE = 7
ERROR_CODE_DECODE = 8
ERROR_CODE_UNKNOWN = 999999


class SpiderError(Exception):
    """ SpiderError """
    def __init__(self, error, message, cause=None):
        """ Constructor """
        self._error = error
        self._cause = cause
        super(SpiderError, self).__init__(message)
        
    @property
    def error(self):
        return self._error
    
    @error.setter
    def error(self, value):
        self._error = value

    @property
    def cause(self):
        return self._cause


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        raise urllib.request.HTTPError(req.get_full_url(), code, msg, headers, fp)
        
        '''
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code        
        return infourl
        '''
    
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    
    
class HttpClient(object):
    """ http client adapter """
    HEADERS = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0"}
    TIMEOUT = 60
    
    def __init__(self):
        """ http client 构造函数 """
        self._timeout = self.TIMEOUT
        self._headers = self.HEADERS
        self._proxy = None
        self._opener = None
        self._auto_redirect = True
    
    @property
    def timeout(self):
        return self._timeout
        
    @timeout.setter
    def timeout(self, value):
        self._timeout = value
 
    @property
    def proxy(self):
        return self._proxy
    
    @proxy.setter
    def proxy(self, value):
        self._proxy = value
        self._opener = None
    
    @property
    def auto_redirect(self):
        return self._auto_redirect
    
    @auto_redirect.setter
    def auto_redirect(self, value):
        self._auto_redirect = value
        
    def _create_opener(self):
        
        cj = http.cookiejar.CookieJar()
        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({self.proxy.protocol: str(self.proxy)})
            if self.auto_redirect:
                opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPCookieProcessor(cj))
            else:
                opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPCookieProcessor(cj), NoRedirectHandler())
        else:
            if self.auto_redirect:
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            else:
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), NoRedirectHandler())
            
        self._opener = opener
           
    @property
    def opener(self):
        if not self._opener:
            self._create_opener()
        return self._opener
       
    @property
    def headers(self):
        return self._headers
    
    @headers.setter
    def headers(self, value):
        self._headers = value
        
    def get(self, url, headers=None):
        """ execute http get method. """
        response = None
        try:
            request = urllib.request.Request(url, headers=headers if headers else self.headers)
            response = self.opener.open(request, timeout=self.timeout)     
            html = response.read()
            return html
        finally:
            if response:
                response.close()

    def post(self, url, params, headers=None):
        """ execute http post method. """
        response = None
        html = None
        while True:
            try:
                request = urllib.request.Request(url, urllib.parse.urlencode(params).encode('UTF-8'), headers=headers if headers else self.headers)
                request.get_method = lambda: 'POST'

                response = self.opener.open(request, timeout=self.timeout)
                # print(response.read())
                html = response.read()
                response.close()
                break

            except urllib.request.HTTPError as e:
                    print( '1:', e)
                    time.sleep(random.choice(range(5, 10)))

            except urllib.request.URLError as e:
                print( '2:', e)
                time.sleep(random.choice(range(5, 10)))
            except socket.timeout as e:
                print( '3:', e)
                time.sleep(random.choice(range(8,15)))
            except socket.error as e:
                print( '4:', e)
                time.sleep(random.choice(range(20, 60)))
            except http.client.BadStatusLine as e:
                print( '5:', e)
                time.sleep(random.choice(range(30, 80)))
            except http.client.IncompleteRead as e:
                print( '6:', e)
                time.sleep(random.choice(range(5, 15)))

        return html
    def download(self, url, output, headers=None):      
        """ download and save it """
        response = None
        try:
            request = urllib.request.Request(url, headers=headers if headers else self.headers)
            response = self.opener.open(request, timeout=self.timeout)            
            with open(output, 'wb') as f:
                f.write(response.read())      
        finally:
            if response:
                response.close()

    def get_redirect(self, url):
        html = None
        try:
            auto_redirect = self.auto_redirect
            
            self.auto_redirect = False
            self.get(url)
            
        except urllib.request.HTTPError as he:

            if he.code > 300 or he.code < 400:
                return he.headers['Location']
            raise he
        
        finally:
            self.auto_redirect = auto_redirect

        return None


if __name__ == '__main__':
    try:
        client = HttpClient()
        print(client.get_redirect('https://www.baidu.com/'))
    except:
        print('aaaaa')