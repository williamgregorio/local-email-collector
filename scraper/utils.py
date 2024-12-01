import requests
import re
from fake_useragent import UserAgent
from urllib.parse import urljoin

def is_scraping_allowed(domain, path, disallowed_paths):
    """
    Will check the specific path is allowed to be scraped based on disallowed paths.
    """
    for disallowed_path in disallowed_paths:
        if path.startswith(disallowed_path):
            return False
    return True

def parse_robots_rules(robots_txt, user_agent="*"):
    """
    Parses the robots.txt for the specified user-agent.
    Returns a list of disallowed paths.
    """
    rules = {}
    current_user_agent = None


def get_headers():
    """
    Generates a 'random' user agent header....
    """
    ua = UserAgent()
    return {'User-Agent': ua.random}

def check_robots(domain):
    """
    Checks disallowed on robots.txt when crawling.
    """
    robots_url = urljoin(domain, '/robots.txt')
    try:
        response = requests.get(robots_url, timeout=7)
        if response.status_code == 200:
            if 'Disallow: /' in response.text:
                print(f"Crawling is disallowed for {domain} by robots.txt")
                return False
        return True
    except Exception as e:
        print(f"Failed to get robots.txt for {domain}: {e}")
