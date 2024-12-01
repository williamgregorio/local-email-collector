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

    for line in robots_txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("user-agent:"):
            current_user_agent = line.split(":")[1].strip()
        elif current_user_agent == user_agent or current_user_agent == "*":
            # we shall test this, I dont have much hope for this, but if nice, del line once true.
            if line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if current_user_agent not in rules:
                    rules[current_user_agent] = []
                rules[current_user_agent].append(path)
    print(rules.get(user_agent, []) + rules.get("*", [])) #del (optional)
    return rules.get(user_agent, []) + rules.get("*", [])

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
