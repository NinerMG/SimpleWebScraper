import unittest
from unittest.mock import patch, Mock, mock_open, call
import requests
from bs4 import BeautifulSoup
import string
import sys
import os

# Add the stage5 directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(__file__))
import stage5


class TestStage5(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_article_list_html = """
        <html>
            <body>
                <article>
                    <span data-test="article.type">News</span>
                    <a data-track-action="view article" href="/articles/test-article-1">Article 1</a>
                </article>
                <article>
                    <span data-test="article.type">Research</span>
                    <a data-track-action="view article" href="/articles/test-article-2">Article 2</a>
                </article>
                <article>
                    <span data-test="article.type">News</span>
                    <a data-track-action="view article" href="/articles/test-article-3">Article 3</a>
                </article>
            </body>
        </html>
        """
        
        self.sample_article_html = """
        <html>
            <head>
                <title>Test Article | Nature</title>
            </head>
            <body>
                <h1>COVID-19 variants show signs of merging | Nature News</h1>
                <div class="article__body">
                    <p>First paragraph of the article content.</p>
                    <p>Second paragraph of the article content.</p>
                </div>
                <p>Regular paragraph not included.</p>
            </body>
        </html>
        """

        self.sample_article_html_alternative = """
        <html>
            <head>
                <title>Test Article | Nature</title>
            </head>
            <body>
                <h1>COVID-19 variants show signs of merging | Nature News</h1>
                <div class="c-article-body">
                    <p>First paragraph using alternative class.</p>
                    <p>Second paragraph using alternative class.</p>
                </div>
            </body>
        </html>
        """
        
        self.sample_article_html_no_body_div = """
        <html>
            <head>
                <title>Test Article | Nature</title>
            </head>
            <body>
                <h1>COVID-19 variants show signs of merging | Nature News</h1>
                <p>First paragraph without body div.</p>
                <p>Second paragraph without body div.</p>
            </body>
        </html>
        """

    @patch('requests.get')
    def test_get_soup_success(self, mock_get):
        """Test successful soup creation."""
        mock_response = Mock()
        mock_response.text = self.sample_article_list_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = stage5.get_soup("https://test.com")
        
        self.assertIsInstance(result, BeautifulSoup)
        mock_get.assert_called_once_with("https://test.com", headers=stage5.HEADERS)
        mock_response.raise_for_status.assert_called_once()
    
    @patch('requests.get')
    def test_get_soup_http_error(self, mock_get):
        """Test soup creation with HTTP error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with self.assertRaises(requests.exceptions.HTTPError):
            stage5.get_soup("https://test.com")
    
    def test_get_all_article_types(self):
        """Test the extraction of all article types."""
        soup = BeautifulSoup(self.sample_article_list_html, 'html.parser')
        
        result = stage5.get_all_article_types(soup)
        
        self.assertIsInstance(result, set)
        self.assertEqual(result, {"News", "Research"})

    def test_get_news_article_links(self):
        """Test extraction of article links for specific article type."""
        soup = BeautifulSoup(self.sample_article_list_html, 'html.parser')
        
        # Test for 'News' type
        news_results = stage5.get_news_article_links(soup, "News")
        expected_news_links = [
            "https://www.nature.com/articles/test-article-1",
            "https://www.nature.com/articles/test-article-3"
        ]
        self.assertEqual(news_results, expected_news_links)
        
        # Test for 'Research' type
        research_results = stage5.get_news_article_links(soup, "Research")
        expected_research_links = [
            "https://www.nature.com/articles/test-article-2"
        ]
        self.assertEqual(research_results, expected_research_links)
    
    def test_get_news_article_links_no_matching_type(self):
        """Test extraction when no articles with matching type are present."""
        soup = BeautifulSoup(self.sample_article_list_html, 'html.parser')
        
        result = stage5.get_news_article_links(soup, "Editorial")
        
        self.assertEqual(result, [])
    

    
    @patch('stage5.get_soup')
    def test_extract_article_content_article_body(self, mock_get_soup):
        """Test article content extraction with article__body class."""
        mock_soup = BeautifulSoup(self.sample_article_html, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage5.extract_article_content("https://test.com/article")
        
        self.assertEqual(filename, "COVID19_variants_show_signs_of_merging.txt")
        expected_content = "First paragraph of the article content.\nSecond paragraph of the article content."
        self.assertEqual(content, expected_content)
    
    @patch('stage5.get_soup')
    def test_extract_article_content_c_article_body(self, mock_get_soup):
        """Test article content extraction with c-article-body class."""
        mock_soup = BeautifulSoup(self.sample_article_html_alternative, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage5.extract_article_content("https://test.com/article")
        
        self.assertEqual(filename, "COVID19_variants_show_signs_of_merging.txt")
        expected_content = "First paragraph using alternative class.\nSecond paragraph using alternative class."
        self.assertEqual(content, expected_content)
    
    @patch('stage5.get_soup')
    def test_extract_article_content_no_body_div(self, mock_get_soup):
        """Test article content extraction with no body div class."""
        mock_soup = BeautifulSoup(self.sample_article_html_no_body_div, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage5.extract_article_content("https://test.com/article")
        
        self.assertEqual(filename, "COVID19_variants_show_signs_of_merging.txt")
        # All paragraphs should be included when no specific body div is found
        expected_content = "First paragraph without body div.\nSecond paragraph without body div."
        self.assertEqual(content, expected_content)
    
    @patch('stage5.get_soup')
    def test_extract_article_content_no_title(self, mock_get_soup):
        """Test article content extraction with no title."""
        html_no_title = "<html><body><p>Content</p></body></html>"
        mock_soup = BeautifulSoup(html_no_title, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage5.extract_article_content("https://test.com/article")
        
        self.assertIsNone(filename)
        self.assertIsNone(content)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_article(self, mock_file):
        """Test saving article to a file."""
        test_content = "This is test article content."
        test_filename = "test_article.txt"
        test_path = "Test_Folder"
        
        stage5.save_article(test_filename, test_content, test_path)
        
        expected_path = os.path.join(test_path, test_filename)
        mock_file.assert_called_once_with(expected_path, "wb")
        mock_file().write.assert_called_once_with(test_content.encode('utf-8'))
    
    @patch('os.makedirs')
    @patch('stage5.save_article')
    @patch('stage5.extract_article_content')
    @patch('stage5.get_news_article_links')
    @patch('stage5.get_all_article_types')
    @patch('stage5.get_soup')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_function_success(self, mock_print, mock_input, mock_get_soup, 
                                  mock_get_types, mock_get_links, mock_extract_content, 
                                  mock_save_article, mock_makedirs):
        """Test the main function execution."""
        # Mock inputs
        mock_input.side_effect = ["2", "News"]
        
        # Mock soup and article types
        mock_soup = Mock()
        mock_get_soup.return_value = mock_soup
        mock_get_types.return_value = {"News", "Research"}
        
        # Mock article links for two pages
        mock_get_links.side_effect = [
            ["https://www.nature.com/articles/test1", "https://www.nature.com/articles/test2"],  # page 1
            ["https://www.nature.com/articles/test3"]  # page 2
        ]
        
        # Mock content extraction
        mock_extract_content.side_effect = [
            ("article1.txt", "Content 1"),
            ("article2.txt", "Content 2"),
            ("article3.txt", "Content 3")
        ]
        
        # Call main function
        stage5.main()
        
        # Verify the number of pages input
        mock_input.assert_has_calls([
            call("Input number of pages to search:\n"),
            call("Enter which type of articles are you interested:\n")
        ])
        
        # Verify folder creation for each page
        mock_makedirs.assert_has_calls([
            call("Page_1", exist_ok=True),
            call("Page_2", exist_ok=True)
        ])
        
        # Verify article extraction and saving
        self.assertEqual(mock_extract_content.call_count, 3)
        self.assertEqual(mock_save_article.call_count, 3)
        
        # Verify final message
        mock_print.assert_any_call("Saved all articles.")
    
    @patch('os.makedirs')
    @patch('stage5.save_article')
    @patch('stage5.extract_article_content')
    @patch('stage5.get_news_article_links')
    @patch('stage5.get_all_article_types')
    @patch('stage5.get_soup')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_function_invalid_input_then_valid(self, mock_print, mock_input, 
                                                   mock_get_soup, mock_get_types, 
                                                   mock_get_links, mock_extract_content, 
                                                   mock_save_article, mock_makedirs):
        """Test main function with invalid input followed by valid input."""
        # Mock inputs: first invalid, then valid
        mock_input.side_effect = ["invalid", "1", "News"]
        
        # Mock other functions
        mock_soup = Mock()
        mock_get_soup.return_value = mock_soup
        mock_get_types.return_value = {"News", "Research"}
        mock_get_links.return_value = ["https://www.nature.com/articles/test1"]
        mock_extract_content.return_value = ("article1.txt", "Content 1")
        
        # Call main function
        stage5.main()
        
        # Verify error message was printed
        mock_print.assert_any_call("Enter number!")
        
        # Verify article was saved
        mock_save_article.assert_called_once()
    
    @patch('os.makedirs')
    @patch('stage5.save_article')
    @patch('stage5.extract_article_content')
    @patch('stage5.get_news_article_links')
    @patch('stage5.get_all_article_types')
    @patch('stage5.get_soup')
    @patch('builtins.input')
    def test_main_function_no_articles(self, mock_input, mock_get_soup, mock_get_types, 
                                      mock_get_links, mock_extract_content, 
                                      mock_save_article, mock_makedirs):
        """Test main function when no articles match the criteria."""
        # Mock inputs
        mock_input.side_effect = ["1", "Editorial"]
        
        # Mock other functions
        mock_soup = Mock()
        mock_get_soup.return_value = mock_soup
        mock_get_types.return_value = {"News", "Research"}
        mock_get_links.return_value = []  # No matching articles
        
        # Call main function
        stage5.main()
        
        # Verify no articles were saved
        mock_extract_content.assert_not_called()
        mock_save_article.assert_not_called()
    
    def test_constants_defined(self):
        """Test that all constants are properly defined."""
        self.assertEqual(stage5.BASE_URL, "https://www.nature.com")
        self.assertTrue(stage5.TARGET_URL.startswith("https://www.nature.com/nature/articles"))
        self.assertIn("Accept-Language", stage5.HEADERS)
        self.assertEqual(stage5.HEADERS['Accept-Language'], 'en-US,en;q=0.5')


if __name__ == '__main__':
    unittest.main()
