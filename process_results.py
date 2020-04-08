import sys
import os
import json
from bs4 import BeautifulSoup

OUT_PATH = "output_csv/"

def get_athlete_soup(big_soup):
    '''Input: 2 element BS list with team and player results
    Output: BS with only athlete results
    Team results in here if we need it later'''
    athlete_soup = []
    for soups in big_soup:
        if 'Academies' in soups.h3.text:
            continue
        else:
            athlete_soup.append(soups)
    return athlete_soup

def bs_str_cleaner(bs_strings):
    '''Input: BS string object
    Output: string stripped of all extra spaces'''
    cleanedstring = ''
    for chars in bs_strings:
        cleanedstring += str(chars).strip()
    return cleanedstring

def process_soup(soup_res):
    '''Input: IBJJF results pages parsed by div class = row
    Output: a list of lists containing tournament, division name, team name and athlete name'''
    team_ind_res_list=[]
    result_list=[]
    row = []
    division_name = ''
    athlete_info= ''
    for m in soup_res:
        if m.h2:
            tournament_name = m.h2.get_text(strip=True)
            pass
        gutted = m.find_all('div', class_='col-xs-12')
        #creates list with (in theory) 2 soup elements: team and player results.
        #MAY NEED TO REVISIT IF RESULTS PAGES ARE FORMATTED DIFFERENT
        for x in gutted:
            team_ind_res_list.append(x)

    #Get BS result excluding team results
    athlete_bs = get_athlete_soup(team_ind_res_list)
    
    for x in athlete_bs:
        divs = x.find_all(['h4', 'div'])
        for y in divs:
            test_text = y.get_text(strip=True)
            if not test_text[0].isdigit():
                division_name = bs_str_cleaner(test_text)
                continue
            if '-' in test_text:
                athlete_info = test_text.split('-')
                row = [tournament_name, division_name]
                for items in athlete_info:
                    items = items.strip()
                    row.append(items)
                result_list.append(row)
    return result_list

def process_results(filename):
    with open(filename, 'r') as file:
        try:
          soup = BeautifulSoup(file.read())
        except:
          raise Exception("failed to parse file: {}".format(filename))

        match = soup.find_all('div',class_='row')
        results = process_soup(match)
    return results

#----begin isaac from process_data.py----
def create_csv(filename, results:list):
  with open(filename, 'w') as outfile:
    for r in results:
      outfile.write(','.join(r)+'\n')

# loop through directory files
def convert_to_csv(path):
  for filename in os.listdir(path):
    # dont process failed files
    print(filename)
    if 'failed' in filename:
      continue
    
    if 'result_1000' in filename:
      res = process_results(path+filename)
      # if array is empty or Nonetype, then dont make a file
      if res:
        if len(res) > 0:
            create_csv(OUT_PATH+filename, res)

#-----end code from process_data.py-----

if __name__ == '__main__':
    convert_to_csv('output/')