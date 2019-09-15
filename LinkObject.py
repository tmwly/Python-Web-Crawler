from _socket import timeout
from urllib import request
from urllib.error import URLError

from requests import HTTPError

# Class used to store a link using the following fields
# url - the url of the link
# count - the number of times the link has been seen in this scrape
# valid - whether the link does not time out or return an error code
# error_reason - the error message returned if the link was not valid
# has_html - whether the link object has the pages html downloaded
# scraped - whether the links html has been fully scraped for new links
# html - the html content of the page at the link


class LinkObject:

    # Constructor
    def __init__(self, url):
        self.url = url
        self.count = 1
        self.valid = False
        self.error_reason = ""
        self.has_html = False
        self.scraped = False
        # self.response initialised later
        # self.valid initialised later

    # Set the links html text and the hasHtml field
    def set_html(self, response):
        self.html = response
        self.has_html = True

    # Set whether the link returned a valid status
    def set_valid(self, valid):
        self.valid = valid

    # Set the reason for the link error
    def set_error_reason(self, error):
        self.error_reason = error

    # Set whether a LinkObject has been fully Scraped
    def set_scraped(self, scraped):
        self.scraped = scraped

    # Increase the number of times this link has been seen
    def increase_count(self):
        self.count += 1

    # Override for default str() method
    def __str__(self):
        s = "URL: " + self.url + \
            "\nScraped: " + self.scraped.__str__() + \
            "\nReference Count: " + self.count.__str__()

        if not self.valid and self.scraped:
            s += "\nError Reason: " + self.error_reason
        return s

    # Checks whether the input URL does not timeout or return an error code, loading it if successful
    def get_response(self):
        try:
            request_item = request.Request(self.url)
            response = request.urlopen(request_item, timeout=5)
            html = response.read().decode('utf-8')

            self.set_html(html)
            self.set_valid(True)

        except (HTTPError, URLError, ValueError) as error:
            self.error_reason = str(error)
        except timeout:
            self.error_reason = 'Socket timed out.'
        except Exception as error:
            self.error_reason = "General error: " + str(error)
