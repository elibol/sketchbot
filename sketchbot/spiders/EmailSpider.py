# -*- coding: utf-8 -*-
"""
"""

import re
from urlparse import urlparse, urljoin

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, TextResponse, XmlResponse

from selenium import webdriver

from sketchbot.items import EmailItem

class EmailSpider(CrawlSpider):
    """
    Spider which collects emails for a given domain.
    """

    name = 'EmailSpider'
    start_urls = None

    # these were pulled from well cited sources on the web
    url_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
                           r"[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    email_regex = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")

    # this is required to follow domain
    # specified through redirects
    first_response = True

    seen = set()

    def __init__(self, URL, *args, **kwargs):
        """
        :param URL: URL/Domain from which to collect emails
        :param args: CrawlSpider args
        :param kwargs: CrawlSpider args
        """
        super(EmailSpider, self).__init__(*args, **kwargs)

        self.logger.debug("URL: %s", URL)

        self.driver = webdriver.Firefox()

        raw_url = URL
        url_parts = urlparse(raw_url)
        if url_parts.scheme == "":
            # try http by default
            raw_url = "http://"+URL
            url_parts = urlparse(raw_url)
        self.domain = url_parts.hostname

        url = url_parts.scheme + "://" + self.domain
        if self.url_regex.match(url) is None:
            raise CloseSpider("Invalid URL.")
        self.start_urls = [url]

        self.seen.add(url)

    def __del__(self):
        self.driver.quit()
        self.driver.close()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def set_domain(self, response):
        """
        Update the domain given the first response.

        :param response: Scrapy Response object.
        :return: None
        """
        url_parts = urlparse(response.url)
        self.domain = url_parts.hostname
        self.logger.debug("default domain: %s", self.domain)

    def parse(self, response):
        """
        Handle the response from the

        :param response: Scrapy Response object.
        :return: None
        """
        if self.first_response:
            self.set_domain(response)
            self.first_response = False

        if urlparse(response.url).hostname != self.domain:
            # this could happen if something from the default
            # subdomain redirects to another subdomain.
            # Example:
            #  Redirecting (302)
            #  to <GET http://spotlight.mit.edu>
            #  from <GET http://web.mit.edu/site/>
            return

        # only consider responses with text
        # would consider something more comprehensive under real circumstances
        if not isinstance(response, (HtmlResponse, TextResponse, XmlResponse)):
            return

        # ignore images
        # would consider something more comprehensive under real circumstances
        content_type = response.headers['Content-Type']
        if content_type.find("image") != -1:
            return

        self.driver.get(response.url)
        root_element = self.driver.find_element_by_xpath("//*")
        rendered_body = root_element.get_attribute("outerHTML")

        # extract emails
        emails = self.email_regex.findall(rendered_body, re.I)
        for email in emails:
            item = EmailItem()
            item['email'] = email
            item['url'] = response.url
            self.logger.info("adding %s", email)
            yield item

        # extract and generate links according to rules
        sel = scrapy.Selector(text=rendered_body)
        for href in sel.xpath('//a/@href').extract():
            url = urljoin(response.url, href)
            url_parts = urlparse(url)
            # control could be handled through Scrapy,
            # but doing so complicates things due to
            # selenium.
            if url_parts.hostname == self.domain and url not in self.seen:
                self.logger.debug((self.domain, url))
                self.seen.add(url)
                yield scrapy.Request(url)
