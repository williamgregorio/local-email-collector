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
    try:
        response = requests.get(robots_url, timeout=7)
        if response.status_code == 200:
            if 'Disallow: /' in response.text:
                print(f"Crawling is disallowed for {domain} by robots.txt")
                return False
        return True
    except Exception as e:
        print(f"Failed to get robots.txt for {domain}: {e}")
