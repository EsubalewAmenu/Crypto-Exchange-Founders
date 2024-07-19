import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from shared import open_browser, load_page, close_driver

    
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