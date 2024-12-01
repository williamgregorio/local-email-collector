import requests
from fake_useragent import UserAgent
from urllib.parse import urljoin

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
