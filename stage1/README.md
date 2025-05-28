# Stage 1 - Dad Joke API Scraper

## Description
This stage is a simple program for fetching jokes from the `icanhazdadjoke.com` API. The program demonstrates the basics of making HTTP requests and working with JSON APIs.

## Features
- **Random joke**: Fetches a random joke from the API
- **Joke by ID**: Allows the user to enter a specific joke ID and retrieve it
- **Error handling**: Checks response validity and handles network errors

## How it works
1. The program asks the user whether they want a random joke or a specific one by ID
2. Depending on the choice:
   - Fetches a random joke, or
   - Asks for an ID input and fetches the specific joke
3. Displays the joke or an error message

## Usage
```bash
python stage1.py
```

## Example output
```
Do you want some random joke or you will try to hit id? yes/no yes
Why don't scientists trust atoms? Because they make up everything!
```

## Requirements
- `requests` - for making HTTP requests