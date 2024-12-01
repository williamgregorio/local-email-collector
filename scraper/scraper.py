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

    def spider_crawl_page(self, url):
        """
        Web crawls one page, extract emails and finds anchors.
        """
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

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
                    self.spider_crawl_page(anchor)
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
        Runs the scraper, by respecting robots.txt if found.
        """
        if not check_robots(self.domain):
            print(f"Will not continue due to robots.txt restrictions as Disallowed.")
            return
        self.spider_crawl_page(self.domain) 
        self.save_to_csv()
        print(f"Email scraping complete. Found {len(self.emails)} emails.")
        print(f"Emails was saved to {self.output_dir}/emails.csv")
