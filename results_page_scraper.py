import sys
import requests
import json
import ast
from bs4 import BeautifulSoup

RESULTS_PAGE_URL = "https://ibjjf.com/results/"

def get_string_request_result(url):
  res = requests.get(url)
  if res.status_code == 200:
    return res.text
  else:
    print("Request failed. Returned: {}".format(res.status_code))
    return res.status_code

# only need to run this once
RESULTS_PAGE_FILENAME = "ibjjf_results_page.txt"
def create_static_results_file():
  s = get_string_request_result(RESULTS_PAGE_URL)
  with open(RESULTS_PAGE_FILENAME, 'w') as outfile:
    outfile.write(s)

# grab only the link URLS and put them in a file
def process_static_results_file():
  with open(RESULTS_PAGE_FILENAME, 'r') as file:
    soup = BeautifulSoup(file.read())
    main_content = soup.find('div', id='mainContent')
    with open("url_list.txt", 'w') as outfile:
      for a in main_content.find_all('a'):
        #print(a['href'])
        outfile.write(a['href']+'\n')

# static.ibjjfdb is pulling a lot of data we already scraped. need to
# cross check the ID in the URL against what we already pulled by looking in /data/verified.txt
def test():
  result = []
  with open("url_list.txt", 'r') as file:
    for line in file:
      if "ibjjf.com/results" in line or "static.ibjjfdb.com" in line:
        result.append(line)
    
    print(result)
    print(len(result))

test()
#process_static_results_file()
