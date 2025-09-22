# 代码生成时间: 2025-09-22 15:02:21
import requests
from bs4 import BeautifulSoup
from celery import Celery
from celery import shared_task
from urllib.parse import urljoin
from django.conf import settings

# Celery configuration
# Assuming that the Celery app is named 'my_app' and the broker URL is in settings
app = Celery('my_app')
app.config_from_object('django.conf:settings', namespace='CELERY')


# Define a Celery task for scraping a single web page
@shared_task(bind=True, default_retry_delay=60)
def scrape_page(self, url):
    """
    Scrape the content of a single web page.

    :param self: Celery task instance
    :param url: URL of the web page to scrape
    :return: Content of the web page
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        # Parse the web page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Here you can add your custom scraping logic, e.g., extracting specific elements
        # For demonstration, we'll just return the entire HTML content
        return soup.prettify()
    except requests.exceptions.RequestException as e:
        # Log the error and retry the task
        self.retry(exc=e)
    except Exception as e:
        # Handle any other exceptions that may occur
        print(f"An unexpected error occurred: {e}")
        return None


# Example usage:
# To scrape a web page, you can call the task like this:
# scrape_page.delay('http://example.com')
