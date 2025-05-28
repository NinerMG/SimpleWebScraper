# Stage 4 - Advanced Nature.com Article Scraper

## Description
The most advanced stage of the project - a complete article scraper for Nature.com. The program automatically finds "News" type articles on a specified page, downloads their content, and saves them to separate text files.

## Features
- **Automatic article detection**: Finds all "News" type articles on the page
- **Link extraction**: Retrieves full URLs to articles
- **Content extraction**: Extracts title and main content of each article
- **Filename cleaning**: Removes punctuation and formats filenames
- **File saving**: Saves each article to a separate .txt file
- **Reporting**: Displays list of saved files

## How it works
1. **Main page fetching**: Connects to Nature.com (page 3, year 2020)
2. **Article filtering**: Finds only articles marked as "News"
3. **Link extraction**: Retrieves full URLs to each article
4. **Article processing**: For each article:
   - Downloads the article page
   - Extracts title from `<h1>` tag
   - Retrieves content from `<p class='article__teaser'>` paragraphs
   - Cleans title to create filename
   - Saves content to file

## Usage
```bash
python stage4.py
```

## Example output
```
Saved articles: ['COVID19_variants_show_signs_of_merging.txt', 'Climate_change_accelerates_in_2020.txt', 'New_telescope_discovers_distant_galaxies.txt']
```

## Output files
- One `.txt` file for each downloaded article
- Filenames are based on article titles (cleaned of special characters)

## Code structure
- `get_soup()` - fetches and parses HTML
- `get_news_article_links()` - finds links to News type articles
- `clean_filename()` - cleans titles for filenames
- `extract_article_content()` - downloads article content
- `save_article()` - saves article to file
- `main()` - orchestrates the entire process

## Requirements
- `requests` - for making HTTP requests
- `beautifulsoup4` - for HTML parsing
- `string` - for filename cleaning

## Configuration
- `BASE_URL`: "https://www.nature.com"
- `TARGET_URL`: Nature.com articles page (year 2020, page 3)
- `HEADERS`: Language settings for better compatibility

## Notes
- Program filters only "News" type articles
- Uses UTF-8 encoding for saved files
- Handles network errors through `response.raise_for_status()`