import html2text
import requests
from bs4 import BeautifulSoup
from random import choice

class Crawler:
    """A simple web crawler to fetch and convert HTML content to plain text."""

    user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0']

    headers = {
    'Authority': 'www.google.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    'Cache-Control': 'max-age=0',
    'User-Agent': choice(user_agents)}

    def __init__(self):
        self.text_maker = html2text.HTML2Text()
        self.text_maker.ignore_links = True
        self.text_maker.ignore_images = True

    def fetch_and_convert(self, url):
        """Fetch the HTML content of a URL and convert it to plain text."""
        try:
            response = requests.get(url, headers=self.headers,timeout=15)
            if response.status_code == 200:
                html_content = response.text
                plain_text = self.text_maker.handle(html_content)
                return plain_text
            else:
                return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    def get_page_html(self, url):
        """Helper method to fetch HTML content of a given URL."""
        try:
            response = requests.get(url, headers=self.headers,timeout=15)
            return response.text if response.status_code == 200 else ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    def google_search(self, query):
        """Perform a Google search and return the search results links in a list."""

        search_results = []
        url = f"https://www.google.com/search?q={query}"
        html = self.get_page_html(url)
        if len(html) == 0:
            return []
        soup = BeautifulSoup(html, "html.parser")

        links = soup.find_all("a", jsname="UWckNb")
        for link in links:
            href = link.get("href")
            if href.find("#:~:text=") != -1:
                href = href.split("#:~:text=")[0]
            if href not in search_results:
                search_results.append(href)

        return search_results

    def write_output(self, search_results):
        """Write the plain text content of search results to text files."""

        count = 0
        for i in search_results:
            count += 1
            try:
                x = self.fetch_and_convert(i)
                if x == "":
                    print(f"Failed to fetch {i}")
                    count -= 1
                    continue
                with open(f"txt_written/link_{count}.txt", "w", encoding="utf-8") as f:
                    f.write(x)
                    x = ""
                    print(f"Written {i} to link_{count}.txt")
            except Exception as e:
                print(f"An error occurred for {i}")
                count -= 1
                continue

            # x = self.fetch_and_convert(i)
            # with open(f"txt_written/link_{count}.txt", "w", encoding="utf-8") as f:
            #     f.write(x)
            #     # print(f"Written {i} to link_{count}.txt")
            #     x = ""

        return f"Written {count} files."