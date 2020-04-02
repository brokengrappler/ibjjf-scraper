import sys
import os
import json
from bs4 import BeautifulSoup

OUT_PATH = "output_csv/"

path = '/Users/paulchung/dropbox (personal)/paul working folder/home/coding/project/ibjjf-scraper/output'
filename = path+'/result_450.txt'

with open(filename, 'r') as file:
    try:
      soup = BeautifulSoup(file.read())
    except:
      raise Exception("failed to parse file: {}".format(filename))
    
    match = soup.find_all('div',class_='row')
    print(len(match))

    for m in match:
        gutted = m.find_all('div', class_='col-xs-12')
        tournament_name = m.h2
        #print(tournament_name)
        
        for x in gutted:
            master_list = []
            if 'Academies' in x.h3.text:
                continue 


def create_csv(filename, results:list):
  with open(filename, 'w') as outfile:
    for r in results:
      outfile.write(','.join(r)+'\n')

# loop through directory files
def convert_to_csv(path):
  for filename in os.listdir(path):
    # dont process failed files
    if 'failed' in filename:
      continue
    
    #if 'registration' or 'result' in filename:
    if 'result_' in filename:
      res = process_test(path+filename)
      # if array is empty or Nonetype, then dont make a file
      if res:
        if len(res) > 0:
          create_csv(OUT_PATH+filename, res)


if __name__=='__main__':
  convert_to_csv('output/')
