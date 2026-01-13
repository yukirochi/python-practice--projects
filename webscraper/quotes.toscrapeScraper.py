import requests
from bs4 import BeautifulSoup
import time
import json


discord_Webhook = 'https://discord.com/api/webhooks/1455196608135434478/PMTw0eUtNbolLx6plkQnXkNT-wtNZx0iqtc4V6LfxI9g533EX1H7uMfHiJQfyRUS_XXX'

def seen():
    try:
      with open ("quotes.json", "r") as f:
          return json.load(f)
    except:
      print('An exception occurred file not found')
      return []

def add(history):
    with open ("quotes.json", 'w') as f:
        json.dump(history, f, indent=4)
def notifydiscord(quote, author):
    if not discord_Webhook:
        return
    
    data = {
        "content": f"🚨 **SNIPER ALERT!** 🚨\n\n**Author:** {author}\n**Quote:** {quote}"
    }
    try:
       requests.post(discord_Webhook, json=data)
    except:
      print('An exception occurred')
    
def scrapebooks():
    url = "http://quotes.toscrape.com/"
    seenquote = seen()
    page_count = 1
    max_page = 10
    target  = 'Albert Einstein'
    while url:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                cont = soup.find_all('div', class_= 'quote')
                
                for i in cont:
                        qoute = i.find('span', class_='text').text
                        author = i.find('small', class_="author").text
                        if author == target:
                            if qoute not in seenquote:
                                    
                                    print(f" -> [NEW DISCOVERY] Found {target}!")
                                    notifydiscord(qoute, author)
                                    seenquote.append(qoute)
                                    add(seenquote)   
                            else:
                                pass                                         
                next_button = soup.find('li', class_='next') 
                if page_count >= max_page:
                     print(f"hanngang page {max_page} lnag po =============================================")
                     url = None
                elif next_button:
                     based_url = "http://quotes.toscrape.com/"
                     next_page = next_button.find("a")['href']
                     url = based_url + next_page
                     page_count += 1
                     time.sleep(1)
                else:
                     url = None   
                    
            else:
                print("failed yung code bai")
                url = None
        except Exception as e:
            print("error po" + e)
            url = None        

if __name__ == "__main__":

    print("--- SNIPER BOT INITIALIZED ---")
    interval = 60
    while True:
        try:
            scrapebooks() 
            
            print(f"Scan complete. Sleeping for {interval} seconds...")
            time.sleep(interval)

        except KeyboardInterrupt:
            print('USER INTERRUPTED')
        except Exception as e:
            print(f"Critical Error: {e}")
            time.sleep(interval)