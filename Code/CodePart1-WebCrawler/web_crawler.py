import os
import csv
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langdetect import detect # doesn't work for this application
from queue import Queue

class WebCrawler:
    def __init__(self, seed_urls, allowed_domains, crawl_id, max_pages=50):
        self.seed_urls = seed_urls
        self.allowed_domains = allowed_domains
        self.max_pages = max_pages
        self.visited_urls = set()
        self.to_crawl = Queue()
        self.repository_path = f"repository_{crawl_id}"
        self.report_file = f"report_{crawl_id}.csv"
        os.makedirs(self.repository_path, exist_ok=True)

    def is_valid_domain(self, url):
        """Check if the URL is within the allowed domain(s)."""
        parsed_url = urlparse(url)
        return any(domain in parsed_url.netloc for domain in self.allowed_domains)

    def download_page(self, url):
        """Download and save the HTML content of the page."""
        try:
            response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
            return None

    def save_page(self, url, content):
        """Save the HTML page to the repository."""
        filename = os.path.join(self.repository_path, f"{hash(url)}.html")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def extract_links(self, html, base_url):
        """Extract and return all valid outlinks from a page."""
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(base_url, link["href"])
            if self.is_valid_domain(absolute_url):
                links.add(absolute_url)
        return links

    def detect_language(self, text):
        """Detect the language of a page."""
        try:
            return detect(text)
        except:
            return "unknown"

    def crawl(self):
        """Crawl web pages starting from the seed URLs."""
        for url in self.seed_urls:
            self.to_crawl.put(url)

        with open(self.report_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["URL", "Outlinks"])

            while not self.to_crawl.empty() and len(self.visited_urls) < self.max_pages:
                url = self.to_crawl.get()
                if url in self.visited_urls:
                    continue

                print(f"Crawling: {url}")
                html_content = self.download_page(url)
                if not html_content:
                    continue

                self.visited_urls.add(url)
                self.save_page(url, html_content)
                outlinks = self.extract_links(html_content, url)

                writer.writerow([url, len(outlinks)])
                
                for link in outlinks:
                    if link not in self.visited_urls:
                        self.to_crawl.put(link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Web Crawler")
    parser.add_argument("-s", "--seeds", nargs="+", required=True, help="List of seed URLs to start crawling from")
    parser.add_argument("-d", "--domains", nargs="+", required=True, help="List of allowed domains for crawling")
    parser.add_argument("-i", "--id", type=str, required=True, help="Unique identifier for this crawl")
    parser.add_argument("--depth", type=int, default=50, help="Maximum number of pages to crawl (default: 50)")
    
    args = parser.parse_args()
    
    crawler = WebCrawler(args.seeds, args.domains, args.id, args.depth)
    crawler.crawl()
    print(f"Crawling completed. Data saved in {crawler.repository_path}/ and {crawler.report_file}")
