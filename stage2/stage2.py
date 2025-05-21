import requests
from bs4 import BeautifulSoup

headers = {'Accept-Language': 'en-US,en;q=0.5'}
url = "https://www.nature.com/articles/d41586-023-00103-3"

response = requests.get(url=url, headers=headers)

if response.status_code != 200:
    print("Invalid input!")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
title_tag = soup.find('title').text
description_tag = soup.find('meta', attrs={'name': 'description'})

if not title_tag or not description_tag:
    print("Invalid input")
    exit()






print({"title": title,})
print({"description": description_label['content']})