import os.path
import string
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.nature.com"
TARGET_URL = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="
HEADERS = {'Accept-Language': 'en-US,en;q=0.5'}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_all_article_types(soup):
    types = set()
    articles = soup.find_all('article')
    for article in articles:
        article_type_tag = article.find('span', {'data-test': 'article.type'})
        if article_type_tag:
            types.add(article_type_tag.text.strip())
    return types

def get_news_article_links(soup, desired_type):
    articles = soup.find_all('article')
    links = []

    for article in articles:
        article_type_tag = article.find('span', {'data-test': 'article.type'})
        if article_type_tag and article_type_tag.text.strip() == desired_type:
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

    body_classes = [
        'c-article-body',
        'article__body',
        'article-item__body',
        'article__content',
        'main-content'
    ]

    paragraphs = []
    for cls in body_classes:
        body = soup.find('div', class_=cls)
        if body:
            paragraphs = body.find_all('p')
            break

    if not paragraphs:
        paragraphs = soup.find_all('p')

    text = "\n".join(p.get_text(strip=True) for p in paragraphs)

    title_tag = soup.find('h1')
    if title_tag:
        raw_title = title_tag.get_text(strip=True).split('|')[0].strip()
        filename = clean_filename(raw_title) + ".txt"
        return filename, text

    return None, None

def save_article(filename, content, path_to_file):
    file_path = os.path.join(str(path_to_file), filename)
    with open(file_path, "wb") as file:
        file.write(content.encode('utf-8'))

def main():
    while True:
        try:
            number_of_pages = int(input("Input number of pages to search:\n"))
            break
        except ValueError:
            print("Enter number!")
    example_soup = get_soup(f"{TARGET_URL}1")
    available_types = get_all_article_types(example_soup)
    print("Available article types on page 1:")
    print(available_types)
    article_type = input("Enter which type of articles are you interested:\n")

    for page in range(1, number_of_pages + 1):
        url = f"{TARGET_URL}{page}"
        soup = get_soup(url)
        article_links = get_news_article_links(soup, article_type)

        folder_name = f"Page_{page}"
        os.makedirs(folder_name, exist_ok=True)
        for link in article_links:
            filename, content = extract_article_content(link)
            if filename and content:
                save_article(filename, content, folder_name)


    print("Saved all articles.")

if __name__ == "__main__":
    main()
