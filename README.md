# Search evaluation dataset - Eva

Creates a search **Eva**luation dataset from Wikipedia text.

## Getting started

Prerequisites

- Python
- Node.js
- Elasticsearch running on localhost:9200

## Scraping and indexing

Install packages:

`$ npm i`

Look through the file `articles.txt` in the articleSampler folder. In there are the Wikipedia pages you will be using to build the dataset.

Navigate to scraper (`$ cd scraper`) folder and run this command:

`$ python scraper.py`

This scrapes the listed Wikipedia pages and puts their texts into a json file.

Next, navigate to root(`$ cd ..`) and run this command:

`$ node createIndex.js` -> This creates an elasticsearch index.

Then run this command:

`$ node indexSomeFiles.js` -> This indexes the Wikipedia text you scraped.

## Creating ground truth file for a query

Queries are on the form \[title/heading1/heading1.5\].
So if you have for example indexed the article https://sv.wikipedia.org/wiki/Polisen_i_Finland we could do searches like this:

`$ node createGroundTruth.js "[Polisen i Finland/Åland]"` -> Serching with query [Polisen i Finland/Åland]

`$ node createGroundTruth.js "[Polisen i Finland]"` -> Serching with query [Polisen i Finland]

`$ node createGroundTruth.js "[Polisen i Finland/Polisens grader och utbildning/Utbildning]""` -> Serching with query [Polisen i Finland/Polisens grader och utbildning/Utbildning]
