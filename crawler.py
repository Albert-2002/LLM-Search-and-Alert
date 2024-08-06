import html2text
import requests
from bs4 import BeautifulSoup
import time

class Crawler:
    def __init__(self):
        self.text_maker = html2text.HTML2Text()
        self.text_maker.ignore_links = True
        self.text_maker.ignore_images = True

    def fetch_and_convert(self, url):
        """Fetch the HTML content of a URL and convert it to plain text."""
        response = requests.get(url)
        time.sleep(5)

        if response.status_code == 200:
            html_content = response.text
            plain_text = self.text_maker.handle(html_content)
            return plain_text
        else:
            return f"Failed to retrieve the URL. Status code: {response.status_code}"

    def get_page_html(self, url):
        """Helper method to fetch HTML content of a given URL."""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        return response.text if response.status_code == 200 else ""

    def google_search(self, query):
        """Perform a Google search and return the search results links."""
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
        count = 0
        for i in search_results:
            count += 1
            x = self.fetch_and_convert(i)
            with open(f"txt_written/link_{count}.txt", "w", encoding="utf-8") as f:
                f.write(x)
                # print(f"Written {i} to link_{count}.txt")
                x = ""
        return f"Written {count} files."

crawler = Crawler()
search_results = crawler.google_search("Coimbatore weather")
# print(search_results)
print(crawler.write_output(search_results))