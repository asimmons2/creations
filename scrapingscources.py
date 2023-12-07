from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup as bs
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
  time.sleep(1.5)
  html = driver.page_source
  soup = bs(html, 'html.parser')
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    driver.quit()
    if soup != None:
      references = soup.find_all('a', class_='abs-redirect-link')
      references = list(references)
      years = []
      links = []
      for i, reference in enumerate(references):
        if i % 2 == 0:
           link = reference['href']
           links.append(link)
           years.append(link[5:9])
      titles = []
      titles = soup.find_all('h3', class_='s-results-title')
      titles = list(titles)
      tlist = []
      for title in titles:
         name = title.text
         tlist.append(name)
      timeline = {} 
      for i in range(len(tlist)):
         if int(years[i]) not in timeline:
            timeline[int(years[i])] = []
         timeline[int(years[i])].append((tlist[i], links[i]))
      sorted_timeline = {k: timeline[k] for k in sorted(timeline)}
      top2 = list(sorted_timeline)[0:2]
      searchnext = [sorted_timeline[k] for k in top2]
      print(searchnext)
      code = [abs_url.split('/')[1] for sublist in searchnext for _, abs_url in sublist]
      print(code)
      



