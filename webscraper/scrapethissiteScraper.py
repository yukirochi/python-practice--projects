import requests
from bs4 import BeautifulSoup


def scrapethis():
      url = 'https://www.scrapethissite.com/pages/'
      headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
      
      try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                  data = BeautifulSoup(response.text, 'html.parser')

                  page = data.find_all('div', class_= 'page')
                  
                  for i in page:
                        title = i.find('h3', class_='page-title').text
                        desc = i.find('p', class_='session-desc').text
                        
                        print(f'title: {title} description: {desc} \n')
                        

      except Exception as e:
            print('error po')                      
if __name__ == '__main__':
      scrapethis()            