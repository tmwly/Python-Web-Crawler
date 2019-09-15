import Scraper

# inputURL = input("Input URL\n")
input_url = "https://news.ycombinator.com/"
input_url = "https://www.bbc.com/"
#input_url = "http://www.learnaltd.com/"

scraper = Scraper

#scraper.run(input_url, 80, False)
scraper.run(input_url, 94, True)


