import requests
from bs4 import BeautifulSoup
import datetime
import re


def get_headers(url):
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    headlines = []
    for headline_tag in soup.find_all(re.compile('^h[1-6]$')):
        headlines.append(headline_tag.text.strip())

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headlines.insert(0, current_datetime)
    return headlines



