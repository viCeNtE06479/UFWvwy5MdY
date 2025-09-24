# 代码生成时间: 2025-09-24 15:33:12
import requests
from bs4 import BeautifulSoup
from celery import Celery

# 配置Celery
app = Celery('web_content_grabber',
             broker='pyamqp://guest@localhost//')

# 函数：抓取网页内容
def fetch_web_content(url):
    """
    Fetches the content of a web page.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# 函数：解析网页内容
def parse_web_content(html_content):
    """
    Parses the HTML content of a web page.

    Args:
        html_content (str): The HTML content of the web page.

    Returns:
        BeautifulSoup: The parsed HTML content.
    """
    try:
        return BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"Failed to parse HTML: {e}")
        return None

# Celery任务：使用Celery异步抓取网页内容并解析
@app.task
def grab_and_parse(url):
    """
    Asynchronously fetches and parses the content of a web page using Celery.

    Args:
        url (str): The URL of the web page to fetch and parse.

    Returns:
        BeautifulSoup: The parsed HTML content of the web page.
    """
    print(f"Fetching and parsing content from {url}")
    html_content = fetch_web_content(url)
    if html_content:
        return parse_web_content(html_content)
    else:
        return None

# 示例用法
if __name__ == '__main__':
    url_to_fetch = 'http://example.com'
    result = grab_and_parse.delay(url_to_fetch)
    print(f"Task started with ID: {result.id}")
    print(f"Task result: {result.get()}")