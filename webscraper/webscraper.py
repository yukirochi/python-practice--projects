import requests
from bs4 import BeautifulSoup
# this is made by gemini
def scrape_books():
    """
    A basic web scraper that fetches book titles from books.toscrape.com
    """
    # 1. The URL we want to scrape (a safe sandbox for practice)
    url = "http://books.toscrape.com/"

    print(f"Scraping {url}...")

    try:
        # 2. Send an HTTP request to the URL
        # The 'headers' help mimic a real browser to avoid being blocked immediately
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        # 3. Check if the request was successful (Status Code 200)
        if response.status_code == 200:
            print("Successfully retrieved the webpage.\n")

            # 4. Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # 5. Find specific data
            # On this site, book articles are in <article class="product_pod">
            articles = soup.find_all('article', class_='product_pod')

            print(f"Found {len(articles)} books on the homepage:\n")

            for article in articles:
                # Extract the title (located in the <h3> tag, inside an <a> tag)
                h3_tag = article.find('h3')
                title = h3_tag.find('a')['title']
                
                # Extract the price (located in <p class="price_color">)
                price = article.find('p', class_='price_color').text

                print(f"- {title} ({price})")
        
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_books()