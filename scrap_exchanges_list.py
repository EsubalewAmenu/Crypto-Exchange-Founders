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
    
def write_to_csv(data, filename='results.csv'):
    file_exists = os.path.isfile(filename)

    # Read existing links to avoid duplicates
    existing_links = set()
    if file_exists:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header if file is not empty
            existing_links = {row[0] for row in reader}  # Collect existing slugs

    # Write new rows
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only if the file did not exist
        if not file_exists:
            writer.writerow(['Slug', 'Name', 'Web', 'X (Twitter)', 'Founders'])

        # Write new data, avoid duplicates
        for url in data:
            slug = url.replace('/exchanges/', '').strip('/')
            if slug not in existing_links:
                writer.writerow([
                    slug, 
                    '',  # Placeholder for 'Name'
                    '',  # Placeholder for 'Web'
                    '',  # Placeholder for 'X (Twitter)'
                    ''   # Placeholder for 'Founders'
                ])
                existing_links.add(slug)

driver = open_browser()

exchanges_url = "https://coinmarketcap.com/rankings/exchanges/"
soup = load_page(driver, exchanges_url, 'button.sc-7d96a92a-0.hOXHRi')
click_show_more(driver, 'button.sc-7d96a92a-0.hOXHRi')
soup = BeautifulSoup(driver.page_source, "html.parser")

scraped_exchanges_urls_data = scraped_exchanges_urls(soup)
write_to_csv(scraped_exchanges_urls_data)

close_driver(driver)