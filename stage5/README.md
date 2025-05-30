# Stage 5 - Multi-page Nature.com Web Scraper

## Description
Stage 5 represents the final and most advanced version of the Nature.com article scraper. This program allows users to search through multiple pages of Nature.com and download articles based on their type. The content is organized into folders by page number, making it easy to manage large collections of articles.

## Features
- **Multi-page scraping**: Allows searching through any number of pages
- **Article type detection**: Identifies all available article types on the website
- **User-defined article filtering**: Lets the user choose which type of articles to download
- **Flexible content extraction**: Supports multiple HTML structures for better compatibility
- **Page-based organization**: Creates separate folders for articles from each page
- **Robust error handling**: Validates user input and handles edge cases

## How it works
1. **User Input**:
   - Asks for the number of pages to search
   - Shows available article types from page 1
   - Lets the user select which article type to download

2. **Article Discovery**:
   - Iterates through each specified page
   - Finds articles matching the specified type
   - Extracts URLs for each matching article

3. **Content Processing**:
   - Creates a folder for each page (`Page_1`, `Page_2`, etc.)
   - For each article:
     - Downloads the full article content
     - Extracts the title from `<h1>` tag
     - Looks for content in various body containers (supports different page layouts)
     - Cleans the title to create a valid filename
     - Saves the content to a text file in the appropriate page folder

## Technical Implementation
- **Adaptive content extraction**: Tries multiple HTML class selectors to support various article formats
- **Robust parsing**: Handles different page structures without breaking
- **Efficient organization**: Groups articles by page number for better management
- **Unicode support**: Properly encodes content for international character support

## Usage
```bash
python stage5.py
```

## Example Interaction
```
Input number of pages to search:
3
Available article types on page 1:
{'News', 'Research', 'Review', 'Editorial', 'Comment'}
Enter which type of articles are you interested:
News
[Articles are downloaded and saved to folders]
Saved all articles.
```

## Project Structure
- **Page_X folders**: Each contains the articles found on page X
- **Article filenames**: Based on the article title with punctuation removed and spaces replaced with underscores

## Dependencies
- requests
- BeautifulSoup4
- os.path
- string
