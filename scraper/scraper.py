import os
import csv
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from scraper.utils import get_headers, check_robots

class EmailScraper:
    def __init__(self, domain):
        self.domain = domain.rstrip('/')
        self.visited_urls = set()
        self.emails = []
        self.output_dir = self.prepare_output_directory()

    def prepare_output_directory(self):
        """
        We will prepare the output directory of data for the domain.
        """
        base_dir = 'emails'
        domain_dir = os.path.join(base_dir, urlparse(self.domain).netloc)
        os.makedirs(domain_dir, exists_ok=True)

    def is_domain_same(self, url):
        """
        Checks if URL is connected to the same domain.
        """
        return urlparse(url).netloc.endswith(urlparse(self.domain).netloc)

    def find_emails(self, text):
        """
        It will find emails in a block of text using this regex.
        """
        email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        return re.findall(email_regex, text)


