from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from bs4 import Tag

TIMEOUT = 60 #seconds
URL = 'https://ui.adsabs.harvard.edu/abs/2023arXiv230508746L/citations'
URL_REFERENCES = 'https://ui.adsabs.harvard.edu/abs/2023arXiv230508746L/references'

# create a Chrome browser object
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

# navigate to the application home page
driver.get(URL_REFERENCES)

# setup a wait condition where we look for the presence of an element before
# code execution continues
try:
  elem = WebDriverWait(driver, TIMEOUT).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'results-list'))
  )
finally:

  # get our page source as a string
  html = driver.page_source

  # load the page source string into beautifulSoup
  page_soup = bs(html, "lxml")

  # start searching...
  container = page_soup.find("ul", {"class": "results-list"})

  for li in container.children:
      
      if isinstance(li, Tag):
          title = li.find('h3')
          print(title.text)

          author_container = li.find('ul', { "class": "just-authors"})

          if author_container != None:

            authors = []
            authors_elements = author_container.find_all('li', { "class" : "article-author" })

            for elem in authors_elements:
                authors.append(elem.text)
            
            # create a string to hold our author names
            names = ""

            # append each author name to the string declared above
            for author in authors:
               names += author + " "

            # print out the names
            print(names)

            # print an empty line just to make the output look nicer
            print("")

# kill the driver process before the program exits
driver.quit()