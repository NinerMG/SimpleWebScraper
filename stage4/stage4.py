import string

import requests
from bs4 import BeautifulSoup

headers = {'Accept-Language': 'en-US,en;q=0.5'}
url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"

response = requests.get(url=url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('article')

base_url = "https://www.nature.com"
news_articles = []
saved_files = []

for article in articles:
    article_type_tag = article.find('span', {'data-test': 'article.type'})
    if article_type_tag and article_type_tag.text.strip() == 'News':
        a_tag = article.find('a', {'data-track-action': 'view article'})
        if a_tag:
            relative_link = a_tag.get('href')
            full_link = base_url + relative_link
            news_articles.append(full_link)

for article in news_articles:
    news_response = requests.get(url=article,headers=headers)
    news_response.raise_for_status()
    news_soup = BeautifulSoup(news_response.text, 'html.parser')

    paragraphs = news_soup.find_all('p', class_='article__teaser')
    text_paragraphs = [p.get_text(strip=True) for p in paragraphs]
    article_text = "\n".join(text_paragraphs)
    title_tag = news_soup.find('h1')
    if title_tag:
        title = title_tag.get_text(strip=True).split('|')[0].strip()
        clean_title = title.translate(str.maketrans('', '', string.punctuation))
        clean_title = clean_title.replace(' ', '_')
        clean_title = clean_title.strip()

        filename = f"{clean_title}.txt"

        with open(filename, "wb") as file:
            file.write(article_text.encode('utf-8'))
            saved_files.append(filename)

print(f"Saved articles: {saved_files}")