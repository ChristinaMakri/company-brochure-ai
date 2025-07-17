import requests
from bs4 import BeautifulSoup
import logging
import os
import hashlib
from utils.config import REQUEST_TIMEOUT, CACHE_ENABLED, CACHE_DIR

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

if CACHE_ENABLED and not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class Website:
    def __init__(self, url):
        self.url = url
        self.body = None
        self.title = "No title found"
        self.text = ""
        self.links = []
        self._fetch()

    def _cache_path(self):
        filename = hashlib.md5(self.url.encode("utf-8")).hexdigest() + ".html"
        return os.path.join(CACHE_DIR, filename)

    def _fetch(self):
        try:
            if CACHE_ENABLED:
                cache_file = self._cache_path()
                if os.path.exists(cache_file):
                    logging.info(f"Loading from cache: {self.url}")
                    with open(cache_file, "rb") as f:
                        self.body = f.read()
                else:
                    logging.info(f"Fetching URL: {self.url}")
                    response = requests.get(self.url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
                    response.raise_for_status()
                    self.body = response.content
                    with open(cache_file, "wb") as f:
                        f.write(self.body)
            else:
                logging.info(f"Fetching URL: {self.url}")
                response = requests.get(self.url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                self.body = response.content
        except requests.RequestException as e:
            logging.error(f"Error fetching {self.url}: {e}")
            self.body = b""

        self._parse()

    def _parse(self):
        if not self.body:
            return
        soup = BeautifulSoup(self.body, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        links = [link.get("href") for link in soup.find_all("a")]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n"
