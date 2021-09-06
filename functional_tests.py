from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
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
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # He types "Buy tiny pink shirt" into a text box
        inputbox.send_keys('Buy tiny pink shirt')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy tiny pink shirt" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy tiny pink shirt', [row.text for row in rows])
        
        # There is still a text box inviting him to add another item.
        # He enters "Wear tiny pink shirt and listen to Wonton Soup"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Wear tiny pink shirt and listen to Wonton Soup')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # The page updates again, and now shows both items on his list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy tiny pink shirt', [row.text for row in rows])
        self.assertIn('2: Wear tiny pink shirt and listen to Wonton Soup', [row.text for row in rows])

        # Little Timmy wonders if the site will remember his list.
        # Then he sees that the site has generated a unique URL for him --
        # there is some explanatory text to that effect.
        self.fail('Finish the test!')
        
        # He visits that URL - his to do list is still there.
        
        # Satisfied, he goes back to sleep.
        
if __name__ == '__main__':
    unittest.main()
