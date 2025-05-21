import requests
from bs4 import BeautifulSoup

headers = {'Accept-Language': 'en-US,en;q=0.5'}
url = "https://www.natre.com/articles/d41586-023-00103-3"

if "nature.com/articles/" not in url:
    print("Invalid page!")
    exit()

response = requests.get(url=url, headers=headers)

if response.status_code != 200:
    print("Invalid page!")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
title_text = soup.find('title').text
description_tag = soup.find('meta', attrs={'name': 'description'})

if not title_text or not description_tag:
    print("Invalid page!")
    exit()


title = title_text.strip()
description = description_tag.get('content', '').strip()



print({"title": title, "description": description})
