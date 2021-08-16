from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Little Timmy has heard about a cool new online to-do app. He goes to check out its homepage
        self.browser.get('http://localhost:8000')
        
        # He notices the page title and header mention to-do lists
        self.assertIn('To Do', self.browser.title)
        self.fail('Finish the test!')
        
        # He is invited to enter a to-do item straight away
        
        # He types "Buy tiny pink shirt" into a text box
        
        # When he hits enter, the page updates, and now the page lists
        # "1: Buy tiny pink shirt" as an item in a to-do list
        
        # There is still a text box inviting him to add another item.
        
        # He enters "Wear tiny pink shirt and listen to Wonton Soup"
        
        # The page updates again, and now shows both items on his list
        
        # Little Timmy wonders if the site will remember his list.
        # Then he sees that the site has generated a unique URL for him --
        # there is some explanatory text to that effect.
        
        # He visits that URL - his to do list is still there.
        
        # Satisfied, he goes back to sleep.
        
if __name__ == '__main__':
    unittest.main()
