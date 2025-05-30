# SimpleWebScraper - Evolution of a Web Scraping Project

This project demonstrates the progressive evolution of a web scraper, starting from a simple API client and advancing to a sophisticated multi-page article downloader. Each stage builds upon the skills and concepts introduced in previous stages, creating a comprehensive learning path for web scraping with Python.

## Project Overview

SimpleWebScraper is a step-by-step web scraping project that develops from basic API interactions to advanced HTML parsing and content organization. The project is organized into 5 stages, each introducing new concepts and techniques:

### Stage 1: Dad Joke API Scraper
**Simple API Client**
- Interacts with the `icanhazdadjoke.com` JSON API
- Demonstrates basic HTTP requests and JSON handling
- Features both random joke retrieval and ID-based lookup
- Introduces proper HTTP headers and response validation

### Stage 2: Nature.com Metadata Extractor
**Basic Web Scraping**
- Moves from API usage to HTML parsing with BeautifulSoup
- Extracts article metadata (title and description) from Nature.com
- Implements URL validation to ensure proper article sources
- Introduces HTML tag selection and content extraction

### Stage 3: HTML Content Saver
**Complete Page Download**
- Downloads entire web pages and saves them locally
- Handles binary file writing and HTTP status codes
- Introduces robust error handling for network and file operations
- Demonstrates complete page preservation techniques

### Stage 4: Advanced Article Scraper
**Targeted Content Extraction**
- Automatically finds and filters articles by type ("News")
- Extracts only relevant content from multiple articles on a page
- Creates cleaned filenames from article titles
- Introduces text cleaning and formatting techniques
- Saves multiple articles to separate files

### Stage 5: Multi-page Nature.com Web Scraper
**Complete Web Scraping Solution**
- Searches across multiple pages based on user input
- Detects available article types and allows user selection
- Organizes downloaded content into page-based folders
- Adapts to various article layouts using flexible selectors
- Demonstrates complete project organization and user interaction

## Technical Evolution

The project shows clear progression in these technical areas:

1. **HTTP Interactions**:
   - Basic API requests (Stage 1) → Complete web page retrieval (Stages 3-5)
   - Simple headers → Language-specific headers for consistent results

2. **Content Processing**:
   - JSON parsing (Stage 1) → Basic HTML extraction (Stage 2) → Complex HTML navigation (Stages 4-5)
   - Single elements → Multiple elements with filtering

3. **File Operations**:
   - No file saving (Stage 1) → Single file (Stage 3) → Multiple files with organization (Stages 4-5)

4. **User Interaction**:
   - Simple binary choice (Stage 1) → Input validation (Stage 5)
   - Fixed targets → User-selected content and scope

5. **Error Handling**:
   - Basic response validation → Comprehensive error handling with fallbacks
   - Single error types → Multiple failure scenarios and recovery

## Dependencies

- **requests**: HTTP client library for making web requests
- **BeautifulSoup4**: HTML parsing and navigation
- **Python standard libraries**: os.path, string

## Usage

Each stage can be run independently:

```bash
# Stage 1: Dad Joke API client
python stage1/stage1.py

# Stage 2: Nature.com metadata extractor
python stage2/stage2.py

# Stage 3: HTML content saver
python stage3/stage3.py

# Stage 4: Advanced article scraper
python stage4/stage4.py

# Stage 5: Multi-page web scraper
python stage5/stage5.py
```

## Testing

Each stage includes comprehensive unit tests that verify functionality and handle edge cases:

```bash
# Run all tests
python run_tests.py

# Or run tests for a specific stage
python -m unittest stage5/test_stage5.py
```

## Project Structure

```
SimpleWebScraper/
├── main.py                  # Project entry point
├── requirements.txt         # Project dependencies
├── run_tests.py            # Test runner
├── TESTING.md              # Testing documentation
├── stage1/                 # Dad Joke API Client
│   ├── README.md           # Stage 1 documentation
│   ├── stage1.py           # Stage 1 implementation
│   └── test_stage1.py      # Stage 1 unit tests
├── stage2/                 # Nature.com Metadata Extractor
│   ├── README.md           # Stage 2 documentation
│   ├── stage2.py           # Stage 2 implementation
│   └── test_stage2.py      # Stage 2 unit tests
├── stage3/                 # HTML Content Saver
│   ├── README.md           # Stage 3 documentation
│   ├── source.html         # Sample output file
│   ├── stage3.py           # Stage 3 implementation
│   └── test_stage3.py      # Stage 3 unit tests
├── stage4/                 # Advanced Article Scraper
│   ├── README.md           # Stage 4 documentation
│   ├── stage4.py           # Stage 4 implementation
│   └── test_stage4.py      # Stage 4 unit tests
└── stage5/                 # Multi-page Web Scraper
    ├── README.md           # Stage 5 documentation
    ├── stage5.py           # Stage 5 implementation
    └── test_stage5.py      # Stage 5 unit tests
```

## Future Improvements

Possible enhancements for the project:
- Command-line arguments for more flexible usage
- Support for additional news sources beyond Nature.com
- Concurrent downloads for better performance
- Data storage in structured formats (CSV, JSON, database)
- Content analysis and categorization
