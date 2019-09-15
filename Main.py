import Scraper

# inputURL = input("Input URL\n")
input_url = "https://news.ycombinator.com/"
#input_url = "https://www.bbc.com/"

scraper = Scraper

scraper.run(input_url, 10, True)


