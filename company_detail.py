import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from shared import open_browser, load_page, close_driver

def scraped_company_data(soup, slug):
        
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

        # Find the <h2> tag with the specific id
        founders_h2 = soup.find('h2', id=f"who-are-the-{slug}-founders")

        # Find all <p> tags after the <h2> and before the next <h2>
        founders_content = []
        for sibling in founders_h2.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name == 'p':
                founders_content.append(sibling.get_text())

        # Join the content of all <p> tags
        founders_text = '\n'.join(founders_content)
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

            # Define the CSS selector for the h2 element by id
            wait_until = f"h2#who-are-the-{row[0]}-founders"

            # Call the scraping function
            soup = load_page(driver, link, wait_until)
            full_scraped_data = scraped_company_data(soup, row[0])

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