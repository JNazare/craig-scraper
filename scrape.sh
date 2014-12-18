#!usr/bin/env bash

# be sure to change both virtualenv directory and scrape/living_social
# directory to where your venv and code is.
cd ~/Users/Juliana/Documents/repos/MediaLab/craigslist_scraper
scrapy crawl craigs -o items.csv -t csv