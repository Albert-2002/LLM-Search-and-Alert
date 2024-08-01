import requests
import html2text

def fetch_and_convert(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        plain_text = text_maker.handle(html_content)
        return plain_text
    else:
        return f"Failed to retrieve the URL. Status code: {response.status_code}"

url = 'https://python.langchain.com/v0.1/docs/use_cases/question_answering/quickstart/'
plain_text = fetch_and_convert(url)
print(plain_text)






