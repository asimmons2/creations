import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://ui.adsabs.harvard.edu/abs/2023arXiv230508746L/citations')
content = r.text
soup = bs(content, 'lxml')

box = soup.find('ul', class_='results-list')
tags = box.find_all('li') # Limit the search to within the 'box' variable

for tag in tags:
  print(tag.text)
