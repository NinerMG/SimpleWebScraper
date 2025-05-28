import unittest
from unittest.mock import patch, Mock, mock_open
import requests
from bs4 import BeautifulSoup
import string
import sys
import os

# Add the stage4 directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(__file__))
import stage4


class TestStage4(unittest.TestCase):
    
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
                <p class="article__teaser">First paragraph of the article content.</p>
                <p class="article__teaser">Second paragraph of the article content.</p>
                <p>Regular paragraph not included.</p>
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
        
        result = stage4.get_soup("https://test.com")
        
        self.assertIsInstance(result, BeautifulSoup)
        mock_get.assert_called_once_with("https://test.com", headers=stage4.HEADERS)
        mock_response.raise_for_status.assert_called_once()
    
    @patch('requests.get')
    def test_get_soup_http_error(self, mock_get):
        """Test soup creation with HTTP error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with self.assertRaises(requests.exceptions.HTTPError):
            stage4.get_soup("https://test.com")
    
    def test_get_news_article_links(self):
        """Test extraction of news article links."""
        soup = BeautifulSoup(self.sample_article_list_html, 'html.parser')
        
        result = stage4.get_news_article_links(soup)
        
        expected_links = [
            "https://www.nature.com/articles/test-article-1",
            "https://www.nature.com/articles/test-article-3"
        ]
        self.assertEqual(result, expected_links)
    
    def test_get_news_article_links_no_news(self):
        """Test extraction when no news articles are present."""
        html_no_news = """
        <html>
            <body>
                <article>
                    <span data-test="article.type">Research</span>
                    <a data-track-action="view article" href="/articles/research-article">Research</a>
                </article>
            </body>
        </html>
        """
        soup = BeautifulSoup(html_no_news, 'html.parser')
        
        result = stage4.get_news_article_links(soup)
        
        self.assertEqual(result, [])
    
    def test_clean_filename(self):
        """Test filename cleaning functionality."""
        test_cases = [
            ("COVID-19: A Global Pandemic!", "COVID19_A_Global_Pandemic"),
            ("Test Article (2023)", "Test_Article_2023"),
            ("Simple Title", "Simple_Title"),
            ("Title with... dots!!!", "Title_with_dots"),
            ("  Spaced  Title  ", "__Spaced__Title__")
        ]
        
        for input_title, expected_output in test_cases:
            with self.subTest(input_title=input_title):
                result = stage4.clean_filename(input_title)
                self.assertEqual(result, expected_output)
    
    @patch('stage4.get_soup')
    def test_extract_article_content_success(self, mock_get_soup):
        """Test successful article content extraction."""
        mock_soup = BeautifulSoup(self.sample_article_html, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage4.extract_article_content("https://test.com/article")
        
        self.assertEqual(filename, "COVID19_variants_show_signs_of_merging.txt")
        expected_content = "First paragraph of the article content.\nSecond paragraph of the article content."
        self.assertEqual(content, expected_content)
    
    @patch('stage4.get_soup')
    def test_extract_article_content_no_title(self, mock_get_soup):
        """Test article content extraction with no title."""
        html_no_title = "<html><body><p class='article__teaser'>Content</p></body></html>"
        mock_soup = BeautifulSoup(html_no_title, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage4.extract_article_content("https://test.com/article")
        
        self.assertIsNone(filename)
        self.assertIsNone(content)
    
    @patch('stage4.get_soup')
    def test_extract_article_content_no_teasers(self, mock_get_soup):
        """Test article content extraction with no teaser paragraphs."""
        html_no_teasers = "<html><body><h1>Title</h1><p>Regular paragraph</p></body></html>"
        mock_soup = BeautifulSoup(html_no_teasers, 'html.parser')
        mock_get_soup.return_value = mock_soup
        
        filename, content = stage4.extract_article_content("https://test.com/article")
        
        self.assertEqual(filename, "Title.txt")
        self.assertEqual(content, "")
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_article_success(self, mock_file):
        """Test successful article saving."""
        test_content = "This is test article content."
        
        stage4.save_article("test_article.txt", test_content)
        
        mock_file.assert_called_once_with("test_article.txt", "wb")
        mock_file().write.assert_called_once_with(test_content.encode('utf-8'))
    
    @patch('stage4.save_article')
    @patch('stage4.extract_article_content')
    @patch('stage4.get_news_article_links')
    @patch('stage4.get_soup')
    @patch('builtins.print')
    def test_main_function_success(self, mock_print, mock_get_soup, mock_get_links, 
                                   mock_extract_content, mock_save_article):
        """Test the main function execution."""
        # Mock the chain of function calls
        mock_soup = Mock()
        mock_get_soup.return_value = mock_soup
        
        mock_get_links.return_value = [
            "https://www.nature.com/articles/test1",
            "https://www.nature.com/articles/test2"
        ]
        
        mock_extract_content.side_effect = [
            ("article1.txt", "Content 1"),
            ("article2.txt", "Content 2")
        ]
        
        # Call main function
        stage4.main()
        
        # Assertions
        mock_get_soup.assert_called_once_with(stage4.TARGET_URL)
        mock_get_links.assert_called_once_with(mock_soup)
        self.assertEqual(mock_extract_content.call_count, 2)
        self.assertEqual(mock_save_article.call_count, 2)
        
        # Check that print was called with saved files
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn("Saved articles:", args)
        self.assertIn("article1.txt", args)
        self.assertIn("article2.txt", args)
    
    @patch('stage4.save_article')
    @patch('stage4.extract_article_content')
    @patch('stage4.get_news_article_links')
    @patch('stage4.get_soup')
    @patch('builtins.print')
    def test_main_function_no_content(self, mock_print, mock_get_soup, mock_get_links,
                                      mock_extract_content, mock_save_article):
        """Test main function when no valid content is found."""
        # Mock the chain with no valid content
        mock_soup = Mock()
        mock_get_soup.return_value = mock_soup
        mock_get_links.return_value = ["https://www.nature.com/articles/test1"]
        mock_extract_content.return_value = (None, None)
        
        # Call main function
        stage4.main()
        
        # Assertions
        mock_save_article.assert_not_called()
        mock_print.assert_called_once_with("Saved articles: []")
    
    def test_constants_defined(self):
        """Test that all constants are properly defined."""
        self.assertEqual(stage4.BASE_URL, "https://www.nature.com")
        self.assertTrue(stage4.TARGET_URL.startswith("https://www.nature.com/nature/articles"))
        self.assertIn("Accept-Language", stage4.HEADERS)
        self.assertEqual(stage4.HEADERS['Accept-Language'], 'en-US,en;q=0.5')


if __name__ == '__main__':
    unittest.main()
