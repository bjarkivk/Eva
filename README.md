# Eva

Creates search **Eva**luation datasets from Wikipedia text.

To run:

Scrape listed wikipedia pages and put them into a json file:
$ python3 scraper.py

If you have elasticsearch running locally on port 9200 this will create an index:
$ node createIndex.js

This will index the wikipedia text you scraped.
$ node indexSomeFiles.js
