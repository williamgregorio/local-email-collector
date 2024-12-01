import os
import csv
import requests
import re
import logging

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from scraper.utils import get_headers, check_robots, is_scraping_allowed, parse_robots_rules
from collections import deque

# For logging actively
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        os.makedirs(domain_dir, exist_ok=True)
        return domain_dir

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

    def spider_crawl_page(self, start_url, disallowed_paths):
        """
        Web crawls pages using (BFS), makes sure pages are visited once, extract emails and finds anchors.
        """
        queue = deque([start_url])

        while queue:
            url = queue.popleft()
            if url in self.visited_urls:
                continue
            self.visited_urls.add(url)
            logging.info(f"Visting: {url}")

            # Checks if path is allowed
            path = urlparse(url).path
            if not is_scraping_allowed(self.domain, path, disallowed_paths):
                print(f"Skipping {url} due to robots.txt restrictions.")
                continue

            try:
                response = requests.get(url, headers=get_headers(), timeout=7)
                soup = BeautifulSoup(response.text, 'html.parser')
            
                # Extracts emails
                found_emails = self.find_emails(response.text)
                for email in found_emails:
                    self.emails.append({'email': email, 'page_found': url})

                # Find anchors
                for a_tag in soup.find_all('a', href=True):
                    anchor = urljoin(url, a_tag['href'])
                    if self.is_domain_same(anchor):
                        self.spider_crawl_page(anchor, disallowed_paths)
            except Exception as e:
                print(f"Error in web crawling {url}: {e}")

    def save_to_csv(self):
        """
        Will save emails to CSV in a domain name specific directory.
        """
        output_file = os.path.join(self.output_dir, 'emails.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['email', 'page_found'])
            writer.writeheader()
            writer.writerows(self.emails)

    def run(self):
        """
        Runs the scraper, by respecting robots.txt when found.
        """
        disallowed_paths = check_robots(self.domain)
        if '/' in disallowed_paths:
            print(f"Will not continue, due to robots.txt global restrictions.")
            return
        self.spider_crawl_page(self.domain, disallowed_paths) 
        self.save_to_csv()
        print(f"Email scraping complete. Found {len(self.emails)} emails.")
        print(f"Emails was saved to {self.output_dir}/emails.csv")
