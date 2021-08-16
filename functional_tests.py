from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

browser = webdriver.Chrome(options=chrome_options)
browser.get('http://localhost:8000')

assert 'Django' in browser.title
