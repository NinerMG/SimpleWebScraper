# SimpleWebScraper - Testing Guide

This project includes comprehensive unit tests for all four stages of the web scraper development.

## Test Structure

Each stage has its own test file:
- `stage1/test_stage1.py` - Tests for Dad Joke API scraper (6 tests)
- `stage2/test_stage2_new.py` - Tests for Nature.com metadata extractor (8 tests)
- `stage3/test_stage3_new.py` - Tests for HTML content saver (10 tests)
- `stage4/test_stage4.py` - Tests for advanced Nature.com article scraper (12 tests)

**Total: 36 tests covering all functionality**

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
Use the provided test runner to run all tests:
```bash
python run_tests.py
```

### Run Individual Stage Tests
Navigate to a specific stage directory and run:
```bash
cd stage1
python test_stage1.py
```

### Run with Verbose Output
```bash
cd stage1
python -m unittest test_stage1.py -v
```

## Test Coverage Summary

### Stage 1 Tests (6 tests) ✅
- ✅ Random joke API requests (success/failure)
- ✅ Joke by ID requests (success/404/invalid)
- ✅ Network error handling
- ✅ Response validation

### Stage 2 Tests (8 tests) ✅
- ✅ Valid Nature.com URL processing
- ✅ Invalid URL domain handling
- ✅ HTTP error responses
- ✅ Missing HTML elements (title/description)
- ✅ BeautifulSoup parsing functionality
- ✅ Headers format validation

### Stage 3 Tests (10 tests) ✅
- ✅ HTTP response handling (200/404/500)
- ✅ File saving functionality
- ✅ Permission error handling
- ✅ Custom filename generation
- ✅ Various status code scenarios
- ✅ Headers and URL format validation

### Stage 4 Tests (12 tests) ✅
- ✅ HTML soup creation and error handling
- ✅ News article link extraction
- ✅ Filename cleaning functionality
- ✅ Article content extraction
- ✅ File saving operations
- ✅ Main function integration
- ✅ Constants validation
- ✅ Edge cases (no content, missing elements)
## Test Features

### Mocking Strategy
- **HTTP Requests**: All external API calls are mocked using `unittest.mock.patch`
- **File Operations**: File I/O operations are mocked to avoid actual file creation
- **User Input**: Input functions are mocked for automated testing
- **Print Statements**: Output is captured and validated

### Test Types
- **Unit Tests**: Individual function testing
- **Integration Tests**: Workflow testing
- **Error Handling**: Exception and edge case testing
- **Configuration Tests**: Constants and settings validation

### Mock Objects Used
- `requests.get()` - For HTTP request mocking
- `builtins.open()` - For file operation mocking  
- `builtins.input()` - For user input mocking
- `builtins.print()` - For output validation

## Expected Test Results

When all tests pass, you should see output similar to:
```
STAGE1     |  6 tests |  0 failures |  0 errors | ✓ PASSED
STAGE2     |  8 tests |  0 failures |  0 errors | ✓ PASSED  
STAGE3     | 10 tests |  0 failures |  0 errors | ✓ PASSED
STAGE4     | 12 tests |  0 failures |  0 errors | ✓ PASSED
--------------------------------------------------
TOTAL      | 36 tests |  0 failures |  0 errors

🎉 All tests passed!
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running tests from the correct directory and that all dependencies are installed.

### Network-Related Test Failures
All network calls are mocked, so tests should not fail due to actual network issues.

### File Permission Errors
File operations are mocked, so tests should not create actual files or encounter permission issues.

## Testing Best Practices

1. **Run tests before making changes** to ensure baseline functionality
2. **Add new tests** when adding new features
3. **Update tests** when modifying existing functionality
4. **Use mocking** to isolate units under test
5. **Test both success and failure scenarios**

## Contributing

When adding new tests:
1. Follow the existing naming convention
2. Include descriptive docstrings
3. Use appropriate mocking for external dependencies
4. Test both success and error conditions
5. Update this documentation
All network calls are mocked, so tests should not require internet connectivity. If network-related tests fail, check the mock configurations.

### File Permission Issues
File operations are mocked in tests, but if running actual code, ensure proper write permissions in the test directories.

## Adding New Tests

To add tests for new functionality:

1. Create test methods following the naming convention `test_functionality_name`
2. Use appropriate mocking for external dependencies
3. Include both success and failure scenarios
4. Add docstrings explaining what each test validates
5. Update this README with new test coverage information

## Continuous Integration

These tests are designed to run in CI/CD environments. The `run_tests.py` script returns:
- Exit code 0: All tests passed
- Exit code 1: One or more tests failed
