import sys
import requests
import json
import ast
import time


class ibjjf_scraper():
  config = {}
  config_filename = 'config.json'
  verified_filename = './data/verified.txt'
  unverified_filename = './data/unverified.txt'
  outfile_template = './output/{prefix}_{id}.txt'
  
  wait_time = 1
  
  verified = []
  unverified = []
  
  last_id_checked = None
  
  url_registration = "https://www.ibjjfdb.com/ChampionshipResults/{id}/PublicRegistrations?lang=en-US"
  url_result = "https://www.ibjjfdb.com/ChampionshipResults/{id}/PublicResults"
  
  id_to_check = []
  batch_size = 200
  
  stats = {
    "ids_checked" : 0
  }
  
  #MAX = 1500
  def __init__(self, batch_size):
    # these files keep track of config settings and what id's we've already checked
    # may not need config for now
    with open(self.config_filename, 'r') as config_file:
      self.config = ast.literal_eval(config_file.read())
    # id returns successful result, add to this list
    with open(self.verified_filename,'r') as verified_file:
      self.verified = ast.literal_eval(verified_file.read())
    # if an id returns noting, these id's should be placed in here
    with open(self.unverified_filename,'r') as unverified_file:
      self.unverified = ast.literal_eval(unverified_file.read())
    # get the last id checked
    #self.last_id_checked = self.config.get('last_id_checked')
    self.batch_size = batch_size


  def populate_list(self, batch_size=25):
    # creates a list of id's to check. batch size determines the number of id's to check
    try:
      self.id_to_check = [id for id in range(self.last_id_checked+1, self.last_id_checked+batch_size)]
    except:
      print('last_id_checked undefined')
      raise


  def process(self):
    self.last_id_checked = max(self.verified + self.unverified)
    self.populate_list(batch_size=self.batch_size)
    for id in self.id_to_check:
      time.sleep(self.wait_time)
      outfile_name = self.outfile_template.format(prefix='result', id=id)
      if not self.scrape_ibjjf(outfile_name=outfile_name, url=self.url_result.format(id=id)):
        self.unverified.append(id)
        continue
      outfile_name = self.outfile_template.format(prefix='registration', id=id)
      if not self.scrape_ibjjf(outfile_name=outfile_name, url=self.url_registration.format(id=id)):
        self.unverified.append(id)
        continue
      self.verified.append(id)
      self.stats['ids_checked'] += 1
    self.wrap_up()


  def scrape_ibjjf(self, outfile_name, url):
    try:
      res = requests.get(url)
      if res.status_code == 200:
        with open(outfile_name, 'w') as outfile:
          outfile.write(res.text)
        return True
      else:
        with open(outfile_name+'.failed', 'w') as outfile:
          outfile.write(res.text)
        return False
    except:
      return False


  def wrap_up(self):
    with open(self.verified_filename,'w') as verified_file:
      verified_file.write(str(self.verified))
    with open(self.unverified_filename,'w') as unverified_file:
      unverified_file.write(str(self.unverified))
    print(self.stats)


if __name__=='__main__':
  try:
    batch_size = int(sys.argv[1])
    time_between_runs = int(sys.argv[2])
    times_to_run = int(sys.argv[3])
  except:
    print("Need 3 arguments as integers: batch size, time between runs (in seconds), number of times to run")
    raise

  s = ibjjf_scraper(batch_size)
  i = 0
  while i < times_to_run:
    s.process()
    time.sleep(time_between_runs)
    i+=1
