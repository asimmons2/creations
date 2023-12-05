from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup as bs
#from urllib import urlopen as ureq
import time

TIMEOUT = 60

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

url = 'https://ui.adsabs.harvard.edu/abs/2023arXiv230508746L/references'
driver.get(url)
try:
  elem = WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'results-list'))
  )
finally:
   html = driver.page_source
   #print(html)
   soup = bs(html, 'html.parser')
   if soup != None:
    references = soup.find_all('a', class_='abs-redirect-link')
    print(references)
    titles = soup.find_all('h3', class_='s-results-title')
    #
    #print(titles)
    #dates = #contained within the link to the abstract -- #abs/2023arXiv230211529P/abstract
    authors = soup.find_all('li', class_='author')
    #print(authors)



