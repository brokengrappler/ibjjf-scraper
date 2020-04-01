import sys
import os
import json
from bs4 import BeautifulSoup

OUT_PATH = "output_csv/"

def process_test(filename):
  with open(filename, 'r') as file:
    try:
      soup = BeautifulSoup(file.read())
    except:
      raise Exception("failed to parse file: {}".format(filename))
    # get tournament name
    tournament = soup.find_all("div", id="content")[0].h2.string.strip()
    # dont process rules seminar registrationas
    if 'Rules Seminar' in tournament or 'Regras' in tournament:
      return
    #get all divisions. divisions identified by <div class='row'> ... </div>
    divisions = soup.find_all("div", class_="row")

    # begin processing entire file. convert each athlete entry into the following format:
    # tournament name, division name, team name, athlete name
    # create a list of lists
    results = []
    for div in soup.find_all("div", class_="row"):
      # <h4> is the division name
      division_name = div.h4.string
      # first <td> has team name, second <td> has athlete name
      for athlete_info in div.find_all("tr"):
        # no athlete info available. skip this row
        if len(athlete_info.find_all("td")) < 2:
          continue
        team, name = athlete_info.find_all("td")
        parsed_team = team.string.strip()
        parsed_name = name.string.strip()
        row = [tournament, division_name, parsed_team, parsed_name]
        results.append(row)

    return results

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
    
    if 'registration' in filename:
      res = process_test(path+filename)
      # if array is empty or Nonetype, then dont make a file
      if res:
        if len(res) > 0:
          create_csv(OUT_PATH+filename, res)


if __name__=='__main__':
  convert_to_csv('output/')
