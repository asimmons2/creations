from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time

TIMEOUT = 60

def scrape_and_find_new_links(url, timeline={}, depth=0, max_depth=3, page_count=0, max_pages=5):
    if depth >= max_depth or page_count >= max_pages:
        return timeline  


    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    soup = None
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'results-list')))
        time.sleep(5) 
        html = driver.page_source
        soup = bs(html, 'html.parser')

        references = soup.find_all('a', class_='abs-redirect-link')
        titles = soup.find_all('h3', class_='s-results-title')
        years = [ref['href'][5:9] for ref in references if ref and 'href' in ref.attrs]
        links = [ref['href'] for ref in references if ref and 'href' in ref.attrs]
        titles = [title.text.strip() for title in titles]

        for year, title, link in zip(years, titles, links):
            if int(year) not in timeline:
                timeline[int(year)] = []
            timeline[int(year)].append((title, link))

        new_codes = [link.split('/')[1] for link in links]

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

    if new_codes:
        page_count += 1

    time.sleep(5)

    base_url = 'https://ui.adsabs.harvard.edu/abs/{}/references'
    for code in new_codes:
        if page_count < max_pages:
            new_url = base_url.format(code)
            return scrape_and_find_new_links(new_url, timeline, depth + 1, max_depth, page_count, max_pages)

    return timeline 

initial_url = 'https://ui.adsabs.harvard.edu/abs/2019NatCo..10.4838./citations'
timeline = scrape_and_find_new_links(initial_url)

sorted_timeline = {k: timeline[k] for k in sorted(timeline)}
print(sorted_timeline)
