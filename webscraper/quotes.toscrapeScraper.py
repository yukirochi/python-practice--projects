import requests
from bs4 import BeautifulSoup

def scrapebooks():
    url = "http://quotes.toscrape.com/"
    
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
        
                print(f"{qoute} by {author}")
        else:
            print("failed yung code bai")
            url = None
    except Exception as e:
        print("error po")
    

if __name__ == "__main__":
    scrapebooks()    