import unittest
from unittest.mock import patch, Mock
import requests
import sys
import os


# Function definitions from stage1.py (copied for testing)
def random_joke_request():
    headers = {'Accept': 'application/json'}
    response = requests.get(url="https://icanhazdadjoke.com", headers=headers)
    data = response.json()
    return data["joke"]


def id_joke_request():
    headers = {'Accept': 'application/json'}
    joke_id = input("Input id of joke:\n")
    try:
        response = requests.get(url=f"https://icanhazdadjoke.com/j/{joke_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "joke" in data:
                return data["joke"]
            else:
                return "Invalid resource"
        else:
            return "Invalid resource!"
    except requests.exceptions.RequestException:
        return "Invalid resource! "


class TestStage1Functions(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_joke_response = {
            "id": "R7UfaahVfFd",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "status": 200
        }
    
    @patch('requests.get')
    def test_random_joke_request_success(self, mock_get):
        """Test successful random joke request."""
        mock_response = Mock()
        mock_response.json.return_value = self.sample_joke_response
        mock_get.return_value = mock_response
        
        result = random_joke_request()
        
        self.assertEqual(result, self.sample_joke_response["joke"])
        mock_get.assert_called_once_with(
            url="https://icanhazdadjoke.com", 
            headers={'Accept': 'application/json'}
        )
    
    @patch('requests.get')
    def test_random_joke_request_network_error(self, mock_get):
        """Test random joke request with network error."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        with self.assertRaises(requests.exceptions.RequestException):
            random_joke_request()
    
    @patch('builtins.input', return_value='R7UfaahVfFd')
    @patch('requests.get')
    def test_id_joke_request_success(self, mock_get, mock_input):
        """Test successful joke request by ID."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_joke_response
        mock_get.return_value = mock_response
        
        result = id_joke_request()
        
        self.assertEqual(result, self.sample_joke_response["joke"])
        mock_get.assert_called_once_with(
            url="https://icanhazdadjoke.com/j/R7UfaahVfFd",
            headers={'Accept': 'application/json'}
        )
    
    @patch('builtins.input', return_value='invalid_id')
    @patch('requests.get')
    def test_id_joke_request_404(self, mock_get, mock_input):
        """Test joke request by ID with 404 response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = id_joke_request()
        
        self.assertEqual(result, "Invalid resource!")
    
    @patch('builtins.input', return_value='test_id')
    @patch('requests.get')
    def test_id_joke_request_missing_joke_key(self, mock_get, mock_input):
        """Test joke request by ID with response missing 'joke' key."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test_id", "status": 200}
        mock_get.return_value = mock_response
        
        result = id_joke_request()
        
        self.assertEqual(result, "Invalid resource")
    
    @patch('builtins.input', return_value='test_id')
    @patch('requests.get')
    def test_id_joke_request_network_error(self, mock_get, mock_input):
        """Test joke request by ID with network error."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        result = id_joke_request()
        
        self.assertEqual(result, "Invalid resource! ")


if __name__ == '__main__':
    unittest.main()
