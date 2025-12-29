from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_datablitz_deals():
    # Target ONLY the specific Nintendo Switch Games Page 2 URL
    urls = [
        "https://ecommerce.datablitz.com.ph/collections/nintendo-switch?page=2&pf_t_categories=Games"
    ]
    
    TARGET_PRICE = 400.00
    
    print("Launching Headless Chrome for DataBlitz Deal Hunt...")

    # 1. Setup Chrome Options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Comment out to debug visually
    
    # Stealth settings
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # Crash fixes
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for url in urls:
            print(f"\n--- Scanning Collection: {url} ---")
            driver.get(url)

            # 2. Wait for Product Grid to Load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "product-item"))
                )
            except:
                print("Could not load product grid for this collection.")
                continue

            # 3. Find all product cards on the page
            products = driver.find_elements(By.CLASS_NAME, "product-item")
            print(f"Found {len(products)} items on page.")

            for product in products:
                try:
                    # Extract Title
                    title_element = product.find_element(By.CLASS_NAME, "product-item__title")
                    title = title_element.text.strip()
                    link = title_element.get_attribute("href")

                    # Extract Price
                    price_element = product.find_element(By.CLASS_NAME, "price")
                    raw_price = price_element.text.strip()
                    
                    # Clean Price Logic
                    clean_string = raw_price.upper().replace('PHP', '').replace('₱', '').replace(',', '').strip()
                    
                    # Handle ranges like "100 - 200"
                    if '-' in clean_string:
                        clean_string = clean_string.split('-')[0].strip()
                    
                    if not clean_string:
                        continue

                    price = float(clean_string)

                    # 4. Check for Deal
                    if price < TARGET_PRICE:
                        print(f" -> [DEAL ALERT] {title}")
                        print(f"    Price: ₱{price}")
                        print(f"    Link: {link}\n")

                except Exception as e:
                    continue
            
            time.sleep(2)

    except Exception as e:
        print(f"Critical Error: {e}")
        driver.save_screenshot("datablitz_error.png")

    finally:
        print("\nScan complete. Closing browser...")
        driver.quit()

if __name__ == "__main__":
    scrape_datablitz_deals()