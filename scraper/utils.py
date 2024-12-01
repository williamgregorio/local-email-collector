import requests
from fake_useragent import UserAgent
from urllib.parse import urljoin

def get_headers():
    ua = UserAgent()
    return {'User-Agent': ua.random}

