from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup as bs
#from urllib import urlopen as ureq
import time
from papers import Paper
from collections import deque, defaultdict

q = deque([])
year_papers = defaultdict(list)
def get_references(paper):
    TIMEOUT = 60
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(paper.link)
    try:
        elem = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'results-list'))
        )
    finally:
        html = driver.page_source
        soup = bs(html, 'html.parser')
        if soup != None:
            references = soup.find_all('a', class_='abs-redirect-link')
            references = list(references)

            this_reference_years = defaultdict(list)
            for i, reference in enumerate(references):
                if i % 2: continue
                reference_id = (reference.text).strip()
                reference_paper = Paper(reference_id)
                reference_paper.link = f'https://ui.adsabs.harvard.edu/abs/{reference_id}/references'
                year = int(reference_id[0:4])
                year_papers[year].append(reference_paper)
                this_reference_years[year].append(reference_paper)
                paper.references.append(reference_id)

            sorted_dict = dict(sorted(this_reference_years.items()))
            c = 0
            #Add oldest 4 papers to queue to explore down the line
            for v in sorted_dict.values():
                for paper in v: 
                    if c > 4: break
                    q.append(paper)
                    c+=1


count = 0

paper = Paper('2023arXiv230508746L')
paper.link = 'https://ui.adsabs.harvard.edu/abs/2023arXiv230508746L/references'
year_papers[2023].append(paper)
q.append(paper)
#while there is a paper to explore and the total number of papers we have looked at is less than some number (3 right now)
while q and count < 3:
    new_paper = q.popleft()
    print(new_paper.id)
    get_references(new_paper)
    count+=1
print(year_papers)