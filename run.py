# -*- coding: utf-8 -*-
"""
Convenience script for running scrape job.
"""

import argparse
import subprocess

if __name__ == "__main__":

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("URL",
                        default="mit.edu",
                        nargs='?',
                        help="domain from which to collect emails")
    PARSER.add_argument("--format", "-t",
                        default="csv",
                        choices=['xml', 'jl', 'json', 'jsonlines', 'csv', 'pickle', 'marshal'],
                        help="storage format")
    ARGS = PARSER.parse_args()

    URL = ARGS.URL
    CMD_STR = ("scrapy crawl EmailSpider -o emails.%s --logfile=scrape.log -t %s -a URL=" + URL)
    CMD = (CMD_STR % tuple([ARGS.format] * 2)).split(" ")
    subprocess.call(CMD)
