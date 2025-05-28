# Stage 3 - HTML Content Saver

## Description
This stage demonstrates downloading entire web page content and saving it to a local file. The program introduces HTTP status code handling and binary data saving.

## Features
- **Content fetching**: Downloads complete HTML content of a web page
- **Status validation**: Checks if the HTTP request was successful (status code 200)
- **File saving**: Saves downloaded data to `source.html` file in binary mode
- **Error handling**: Checks response codes and handles file writing errors

## How it works
1. Makes a GET request to a specified URL (Facebook in this case)
2. Checks if the response code is HTTP 200 (OK)
3. If successful - saves the entire content to `source.html` file
4. Handles network errors and file system errors (e.g., permission issues)

## Usage
```bash
python stage3.py
```

## Example output
```
Content saved.
```

## Output files
- `source.html` - contains the downloaded HTML content of the page

## Requirements
- `requests` - for making HTTP requests

## Notes
- The program has two defined URLs: one working (`url_ok`) and one invalid (`url_bad`)
- Currently uses `url_ok` (Facebook)
- Saves data in binary mode to preserve original encoding