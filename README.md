# Python-Web-Scraper
This is a basic web scraper written in Python. 

It accepts a starting URL, downloads it,  and from that finds every  `href="http://www.example.com"` inside of a `<a>` tag. It adds each link to a dictionary containing the set of seen links. Finally it performs a search on all returned links in the initial page until it has found a set number of unique links. Once the search is complete, the links are printed to the screen. 

Each link is filtered to ensure formatting is consistent, and that any relative references are saved as the absolute URI.

The filtering removes the following links:

- In page  links using #
`http://www.example.com#about-us`
- In page links using ?
`http://www.example.com?username=test`
- Mailto links
`href="maito:me@email.com"`

All link matching and filtering is done with Regex.

The scraper has methods for both breadth first and depth first searching of links.
