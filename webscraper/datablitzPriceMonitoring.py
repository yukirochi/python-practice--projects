from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time
import requests
import os

load_dotenv()

discord_Webhook = os.getenv("discordhook")
current_price = None

def discord(target,price, link=None):
    if not discord_Webhook:
        return
 
    data = {
        'content': f"🚨 **PRICE CHANGE ALERT** 🚨\n\nThe **{target}** is currently at **{price}** and the link is: {link}"
    }
    try:
        requests.post(discord_Webhook, json=data)
        print(f" -> Sent Discord alert for {target}")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

def scrape(url, last_price):
   
    print(f"Checking...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Runs in background (invisible)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None   
    new_price = last_price
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        fresh_price = soup.find('span', class_='price')
        price = soup.find('span', class_='price').text.strip().replace('₱', '').replace(',', '')
        name = soup.find('h1', class_='product-meta__title').text.strip()
        current_price = float(price)
        if float(price) != current_price:
            discord(name, current_price, url)
            print(f" -> Price changed to {new_price} for {name}")
            new_price = float(price)
        else:
            print(f"No change. Still {fresh_price.text.strip()}")
            new_price = last_price   

    except Exception as e:
        print(f"An exception occurred: {e}")

    finally:
        if driver:
            driver.quit()

    return new_price           
        

    
if __name__ == "__main__":
    url = input("Enter the Datablitz Product URL to scrape (e.g., games, consoles): ").strip()
    current_tracked_price = None 

    print("--- Monitoring Started (Press Ctrl+C to stop) ---")
    while True:
        current_tracked_price = scrape(url, current_tracked_price)
        time.sleep(300)  # Wait for 5 minutes before checking again    