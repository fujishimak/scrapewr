# scrapewr
A Python-based scraper for Sam Nabi's blog.

Uses requests and BS4 to fetch all links from the blog. Then performs duplicate detection against an existing flat file database of links prior to updating. Leverages the Configparser module as well for this.
