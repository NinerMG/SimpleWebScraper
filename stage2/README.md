# Stage 2 - Nature.com Metadata Extractor

## Description
This stage introduces web scraping using BeautifulSoup to extract metadata from Nature.com articles. The program fetches and displays the title and description of an article.

## Features
- **URL validation**: Checks if the URL contains "nature.com/articles/"
- **Metadata extraction**: Extracts title and description from HTML tags
- **Error handling**: Checks HTTP response codes and presence of required elements

## How it works
1. Validates that the provided URL is a valid Nature.com article address
2. Makes an HTTP request with appropriate language headers
3. Parses HTML using BeautifulSoup
4. Extracts title from `<title>` tag and description from meta `description` tag
5. Displays the result in dictionary format

## Usage
```bash
python stage2.py
```

## Example output
```python
{
    'title': 'How AI is revolutionizing scientific research | Nature',
    'description': 'Artificial intelligence is transforming how scientists conduct research...'
}
```

## Requirements
- `requests` - for making HTTP requests
- `beautifulsoup4` - for HTML parsing

## Notes
- URL is hardcoded in the script
- Program exits if the page is invalid