# Summary
This program scrapes email addresses from a specific domain.
By default, scraped email addresses are stored as csv files in `emails.csv`,
along with the url from which they were scraped.

# Install
* `pip install -r requirements.txt`

# Run
* Full command: `scrapy crawl emailcrawler -o emails.csv --logfile=scrape.log -t csv -a URL=mit.edu`
* Convenience script: `python run.py mit.edu -t csv`

Monitor logs with `tail -f scrape.log | grep EmailSpider`.

# TODO

* Improve filters based on content type and response type.
* Use scrapy abstractions for "seen" urls.
* Test "seen" urls.
* Comprehensive filter for removing false positives.
* Improve email extraction (are we using the optimal pattern?).
* Improve link extraction (do better than just pulling href).
* Improve integration between selenium and scrapy.