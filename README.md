# Eva

Creates search **Eva**luation datasets from Wikipedia text.

## To run:

Prerequisites:

- Python
- Node.js
- Elasticsearch running on localhost:9200

Install packages:

`$ npm i`

Navigate to scraper folder. Scrape listed wikipedia pages and put them into a json file:

`$ python3 scraper.py`

Navigate to root. Create an index:

`$ node createIndex.js`

Index the wikipedia text you scraped.

`$ node indexSomeFiles.js`
