import string
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.nature.com"
TARGET_URL = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
HEADERS = {'Accept-Language': 'en-US,en;q=0.5'}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_news_article_links(soup):
    articles = soup.find_all('article')
    links = []

    for article in articles:
        article_type_tag = article.find('span', {'data-test': 'article.type'})
        if article_type_tag and article_type_tag.text.strip() == 'News':
            a_tag = article.find('a', {'data-track-action': 'view article'})
            if a_tag:
                relative_link = a_tag.get('href')
                full_link = BASE_URL + relative_link
                links.append(full_link)
    return links

def clean_filename(title):
    title = title.translate(str.maketrans('', '', string.punctuation))
    title = title.replace(' ', '_').strip()
    return title

def extract_article_content(article_url):
    soup = get_soup(article_url)

    paragraphs = soup.find_all('p', class_='article__teaser')
    text = "\n".join(p.get_text(strip=True) for p in paragraphs)

    title_tag = soup.find('h1')
    if title_tag:
        raw_title = title_tag.get_text(strip=True).split('|')[0].strip()
        filename = clean_filename(raw_title) + ".txt"
        return filename, text
    return None, None

def save_article(filename, content):
    with open(filename, "wb") as file:
        file.write(content.encode('utf-8'))

def main():
    soup = get_soup(TARGET_URL)
    article_links = get_news_article_links(soup)

    saved_files = []
    for link in article_links:
        filename, content = extract_article_content(link)
        if filename and content:
            save_article(filename, content)
            saved_files.append(filename)

    print(f"Saved articles: {saved_files}")

main()
