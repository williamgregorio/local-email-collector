import os
import csv
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from scraper.utils import get_headers, check_robots


