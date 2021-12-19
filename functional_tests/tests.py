from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
	def setUp(self):
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		self.browser = webdriver.Chrome(options=chrome_options)
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_layout_and_styling(self):
		# Little Timmy goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# He notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

		# He starts a new list and sees the input is nicely centered there too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

	def test_can_start_a_list_for_one_user(self):
		# Little Timmy has heard about a cool new online to-do app. He goes to check out its homepage
		self.browser.get(self.live_server_url)
        	
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
		self.wait_for_row_in_list_table('1: Buy tiny pink shirt')
		
		# There is still a text box inviting him to add another item.
		# He enters "Wear tiny pink shirt and listen to Wonton Soup"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Wear tiny pink shirt and listen to Wonton Soup')
		inputbox.send_keys(Keys.ENTER)
		
		# The page updates again, and now shows both items on his list
		self.wait_for_row_in_list_table('1: Buy tiny pink shirt')
		self.wait_for_row_in_list_table('2: Wear tiny pink shirt and listen to Wonton Soup')
		
		# Satisfied, he goes back to sleep.

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Little Timmy starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy tiny pink shirt')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy tiny pink shirt')
		
		# He notices that his list has a unique URL
		little_timmy_list_url = self.browser.current_url
		self.assertRegex(little_timmy_list_url, '/lists/.+')
		
		# Now a new user, Big Tim comes along to the site.
		
		## We use a new browser session to make sure that no information
		## of Little Timmy's is coming through from cookies etc
		self.browser.quit()
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		self.browser = webdriver.Chrome(options=chrome_options)
		
		# Big Tim visits the home page. There is no sign of Little Timmy's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy tiny pink shirt', page_text)
		self.assertNotIn('listen to Wonton Soup', page_text)
		
		# Big Tim starts a new list by entering a new item. He
		# is upset with his situation...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy cigarettes')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy cigarettes')
		
		# Big Tim gets his own unique URL
		big_tim_list_url = self.browser.current_url
		self.assertRegex(big_tim_list_url, '/lists/.+')
		self.assertNotEqual(big_tim_list_url, little_timmy_list_url)
		
		# Again, there is no trace of Little Timmy's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy tiny pink shirt', page_text)
		self.assertIn('Buy cigarettes', page_text)
		
		# Satisfied, they both go back to sleep
