import html2text
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def fetch_and_convert(url):
    """Fetch the HTML content of a URL and convert it to plain text."""

    response = requests.get(url)
    time.sleep(5)

    if response.status_code == 200:
        html_content = response.text
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True
        plain_text = text_maker.handle(html_content)
        return plain_text
    else:
        return f"Failed to retrieve the URL. Status code: {response.status_code}"

def get_page_html(url):
    """Get the HTML content of a page using Playwright."""

    with sync_playwright() as playwright:
        try:
            chromium = playwright.chromium
            browser = chromium.launch(headless=True)
            page = browser.new_page()
            res = page.goto(url)
            if not res.ok:
                return ""
            page.wait_for_selector('body')
            page.wait_for_timeout(3000)
            html = page.content()
            page.close()
            return html
        except:
            return ""

def google_search(query):
    """Perform a Google search and return the search results links."""

    search_results = []
    url = f"https://www.google.com/search?q={query}"
    html = get_page_html(url)
    if len(html) == 0:
            return []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a",jsname="UWckNb")
    for link in links:
        href = link.get("href")
        if href.find("#:~:text=") != -1:
            href = href.split("#:~:text=")[0]
        if href not in search_results:
            search_results.append(href)

    return search_results

def write_output(search_results):
    count = 0
    for i in search_results:
        count += 1
        x = fetch_and_convert(i)
        with open(f"txt_written/link_{count}.txt", "w", encoding="utf-8") as f:
            f.write(x)
            # print(f"Written {i} to link_{count}.txt")
            x = ""
    return f"Written {count} files."

# print(write_output(google_search("Python")))

# print(google_search("Python"))

# x = fetch_and_convert('https://www.codecademy.com/catalog/language/python')
# with open("txt_written/codecademy_python.txt", "w", encoding="utf-8") as f:
#     f.write(x)