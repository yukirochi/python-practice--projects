from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
from dotenv import load_dotenv
import os
load_dotenv()

discord_Webhook = os.getenv("discordhook")

def discord(target, price, link=None):
    if not discord_Webhook:
        return
 
    data = {
        'content': f"🚨 **DEAL ALERT** 🚨\n\nThe **{target}** is currently at **{price}** and the link is: {link}"
    }
    try:
        requests.post(discord_Webhook, json=data)
        print(f" -> Sent Discord alert for {target}")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

def scrape():
    #base_url = 'https://ecommerce.datablitz.com.ph/collections/games'
    base_url = input("Enter the Datablitz collection URL to scrape (e.g., games, consoles): ").strip()
    target_price = input("Enter the target price (e.g., 1000): ").strip()
    page = 1
    
    if '?page=' in base_url:
        base_url = base_url.split('?page=')[0]

    # --- SELENIUM SETUP ---
    # We use Selenium just to fetch the page because requests is being blocked
    print("Launching Chrome...")
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment to hide the browser window
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Run loop for 10 pages
    while page <= 10:
        current_url = f"{base_url}?page={page}"
        print(f"Scanning Page {page}: {current_url}")
        
        try:
            # 1. FETCH with Selenium
            driver.get(current_url)
            
            # Wait a moment for the page to fully load
            time.sleep(5)
            
            # 2. HANDOFF to BeautifulSoup
            # We grab the HTML from the browser and give it to BS4
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 3. PARSE with BeautifulSoup (Your original logic)
            cont = soup.find_all("div", class_='product-item')
            
            if not cont:
                print("No products found. Checking selectors...")
            
            
            for i in cont:
                price_tag = i.find('span', class_='money')
                name_tag = i.find('a', class_='product-item__title')
                link = i.find('a', class_='product-item__title')
                
                if price_tag and name_tag:
                    raw_price = price_tag.text.strip()
                    product_name = name_tag.text.strip()
                    product_link = "https://ecommerce.datablitz.com.ph" + link['href'] if link else "No link available" 
                    # Clean the price
                    clean_price_str = raw_price.replace('₱', '').replace(',', '').strip()
                    clean_price_str = clean_price_str.replace('PHP', '').strip()

                    try:
                        price = float(clean_price_str)
                        
                        if 'Pre-Order' not in product_name:
                        # Alert if price > 500
                            if price <= int(target_price):
                                discord(product_name, raw_price, product_link)
                    except ValueError:
                        continue
            
            page += 1

        except Exception as e:
            print(f"An exception occurred: {e}")
            break
            
    # Close browser when done
    driver.quit()

if __name__ == "__main__":
    scrape()