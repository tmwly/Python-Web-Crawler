import Scraper

# inputURL = input("Input URL\n")
input_url = "https://news.ycombinator.com/news/"
#input_url = "https://www.bbc.com"

scraper = Scraper
scraper.run_breadth_first(input_url, 500, False, True)
scraper.clear_results()
scraper.run_depth_first(input_url, 500, False, True)


