import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import csv
from shared import open_browser, load_page, close_driver
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait



def click_show_more(driver, show_more_selector):
    try:
        while True:
            # Find the "Show More" button
            
            show_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, show_more_selector)))
            show_more_button.click()
            
            # Wait for AJAX content to load (you may need to adjust this wait time based on your application)
            time.sleep(2)  # Adjust as needed
            
            # You can add more specific checks here based on your application
            # For example, check if new content has loaded or if the button disappears
            
            # Check if the "Show More" button still exists
            try:
                driver.find_element(By.CSS_SELECTOR, show_more_selector)
            except NoSuchElementException:
                break  # If the button is not found, exit the loop
            
    except TimeoutException:
        print("Timeout waiting for Show More button.")

def scraped_exchanges_urls(soup):
    links = []
    for a_tag in soup.find_all('a', href=True):
        if a_tag['href'].startswith('/exchanges/'):
            links.append(a_tag['href'])
    return links
    
driver = open_browser()

exchanges_url = "https://coinmarketcap.com/rankings/exchanges/"
soup = load_page(driver, exchanges_url, 'button.sc-7d96a92a-0.hOXHRi')
click_show_more(driver, 'button.sc-7d96a92a-0.hOXHRi')
soup = BeautifulSoup(driver.page_source, "html.parser")

scraped_exchanges_urls_data = scraped_exchanges_urls(soup)