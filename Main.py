import Scraper

# inputURL = input("Input URL\n")
input_url = "https://news.ycombinator.com/news/"

scraper = Scraper
scraper.run_default_bf(input_url)
scraper.clear_results()
scraper.run_default_df(input_url)


