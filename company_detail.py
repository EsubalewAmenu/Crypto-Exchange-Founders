import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from shared import open_browser, load_page, close_driver
import re
import unicodedata


def scraped_company_data(soup):
        
    try:
        name = soup.find('h1', class_='sc-aba8b85a-0 sc-d36bb8b9-3 SZLGM lpefGs').text.strip()
    except AttributeError:
        name = None

    try:
        first_a_tag = soup.find('ul', class_='cmc-details-panel-links').find('a')

        # Extract the URL
        website_url = first_a_tag['href'] if first_a_tag else None
    except AttributeError:
        website_url = None

    try:
        twitter_url = soup.find('a', href=lambda href: href and "twitter.com" in href).get('href')
    except AttributeError:
        twitter_url = None

    try:

        possible_ids = [
                f"who-are-the-{custom_slugify(name)}-founders",
                f"who-are-the-founders-of-{custom_slugify(name)}"
            ]

        
        # Find the target <h2> element with any of the possible ids
        founders_h2 = next((soup.find('h2', id=element_id) for element_id in possible_ids if soup.find('h2', id=element_id)), None)

        # Find the next <h2> after the target <h2>
        next_h2 = founders_h2.find_next_sibling('h2')
        
        # Get all siblings of the target <h2>
        siblings = founders_h2.find_next_siblings()
        
        # Collect <p> tags between the target <h2> and the next <h2>
        founders_text = []
        for sibling in siblings:
            if sibling == next_h2:
                break
            if sibling.name == 'p':
                founders_text.append(sibling.text)
        founders_text = '\n'.join(founders_text)
    except AttributeError:
        founders_text = None

    return {
        'name': name,
        'website': website_url,
        'twitter': twitter_url,
        'founders': founders_text,
    }
    
def read_and_process_csv(filename='results.csv'):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header
        rows = list(reader)  # Read the remaining rows

    driver = open_browser()

    updated_rows = []
    for row in rows:
        # Skip empty rows
        if not row or len(row) < 3:
            updated_rows.append(row)
            continue
        
        name = row[1]
        link = "https://coinmarketcap.com/exchanges/"+row[0]
        print("Scraping ", link, "started!")
        
        # Check if the name column is empty
        if not name:

            # Call the scraping function
            soup = load_page(driver, link, "h1.sc-aba8b85a-0.sc-d36bb8b9-3.SZLGM.lpefGs")
            full_scraped_data = scraped_company_data(soup)

            # Update the row with the scraped data
            row[1] = full_scraped_data.get('name', '')
            row[2] = full_scraped_data.get('website', '')
            row[3] = full_scraped_data.get('twitter', '')
            row[4] = full_scraped_data.get('founders', '')
            
        updated_rows.append(row)

    close_driver(driver)

    # Write the updated rows back to the CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(updated_rows)

read_and_process_csv()