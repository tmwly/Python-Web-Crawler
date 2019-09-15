from _socket import timeout
from urllib import request
from urllib.error import URLError

from requests import HTTPError


class LinkObject:
    def __init__(self, url):
        self.url = url
        self.count = 1
        self.valid = False
        self.ErrorReason = ""
        self.hasHtml = False
        self.scraped = False
        # self.response initialised later
        # self.valid initialised later

    def set_html(self, response):
        self.html = response
        self.hasHtml = True

    def set_valid(self, valid):
        self.valid = valid

    def set_error_reason(self, error):
        self.ErrorReason = error

    def increase_count(self):
        self.count += 1

    def set_scraped(self, scraped):
        self.scraped = scraped

    def __str__(self):
        s = "URL: " + self.url + \
            "\nScraped: " + self.scraped.__str__() + \
            "\nReference Count: " + self.count.__str__()

        if not self.valid and self.scraped:
            s += "\nError Reason: " + self.ErrorReason
        return s

# checks whether the input URL is does not timeout and returns code 200,
# if success, sets global_first variable to response
    def get_response(self):
        try:
            request_item = request.Request(self.url)
            response = request.urlopen(request_item, timeout=5)
            html = response.read().decode('utf-8')

            self.set_html(html)
            self.set_valid(True)

        except (HTTPError, URLError, ValueError) as error:
            self.ErrorReason = str(error)
        except timeout:
            self.ErrorReason = 'socket timed out'
        except Exception as error:
            self.ErrorReason = "BIG ERROR : " + str(error)
