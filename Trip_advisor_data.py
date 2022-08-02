from typing import Dict
from bs4 import BeautifulSoup
import requests
import base64
import json

# request config
user_agent = {'User-agent': 'Mozilla/5.0'}
url = "https://www.tripadvisor.fr/Hotel_Review-g295424-d302457-Reviews-Burj_Al_Arab-Dubai_Emirate_of_Dubai.html"

req = requests.get(url, headers=user_agent)

# parsing data
page = req.content
soup = BeautifulSoup(page, 'lxml')

page_data = {
    'Page name' : '',
    'URL Page' : '',
    'number of comments' : '',
    'Address': '',
    'Telephone' : '',
    'Site web' : '',
    'comments' : []
}

comment = {
    'Author' : '',
    'Title' : '',
    'nb contributions' : '',
    'Date commentaire' : '',
    'Text' : '',
    'date de sejour' : ''
}
# find all comments div
com_div = soup.find_all('div', {'class':'cWwQK MC R2 Gi z Z BB dXjiy', 'data-test-target':'HR_CC_CARD'})

# getting general page data
page_data['Page name'] = soup.find('title').text
page_data['URL Page'] = req.url
page_data['number of comments'] = len(com_div)
page_data['Address'] = soup.find('span', class_='ceIOZ yYjkv').text
page_data['Telephone'] =soup.find('span', class_='eeFQx ceIOZ yYjkv').text

# the URL was encypted so i have tried to decode it and clean it.
encoded_url = soup.find('a', {'class':'dOGcA Ci Wc _S C dCQWE _S eCdbd GlpQN', 'target':'_blank'}).attrs['data-encoded-url']
decoded_url = base64.b64decode(encoded_url).decode("utf-8")

page_data['Site web'] = 'https://www.tripadvisor.fr' + decoded_url[4:]


# comments data 
for com in com_div:
    comment = dict(comment)
    comment['Author'] = com.find('a', class_='ui_header_link bPvDb').text
    comment['Title'] = com.find('div', {'class':'fpMxB MC _S b S6 H5 _a', "dir": "ltr"}).text
    comment['nb contributions'] = (com.find('span', class_="eUTJT").text).split()[0]
    # my logic to get the proper date commentaire
    raw = com.find('div', 'bcaHz').text
    pos = raw.find('(') 
    comment['Date commentaire'] = (com.find('div', 'bcaHz').text)[pos+1:-1]
    comment['Text'] = com.find('q', class_="XllAv H4 _a").text
    comment['date de sejour'] = com.find('span', class_="euPKI _R Me S4 H3").text[17:]
    
    page_data['comments'].append(comment)
    

def save_data(data):
    with open("Hotel_burj_arab.json", "w", encoding= 'utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Data saved Successfully!")


# saving data in JSON file
save_data(page_data)
