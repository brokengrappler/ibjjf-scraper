# ibjjf-scraper

To start, run setup shell script

```
./setup.sh
```

## Usage

positional arguments:
1. batch size
number of tournament id's to check

2. time between runs (in seconds)
number of seconds between execution of scraper

3. number of times to run

```
python3 ibjjf_scraper.py 100 3600 3
```

the script makes one request call per second. the batch size (first argument) determines how many calls in a row it will make for each run. after finishing a batch, it will wait for the number of seconds defined by the second argument before it tries another batch. the third argument determines how many runs the script will make.

in the example above, the script will make 100 calls per batch, wait 1 hour between batches, and run 3 total batches (in other words, 300 request calls over 3 hours). this is pretty conservative

the purpose of these arguments is to get around scraping call limits. we do not know what the limits for the number of calls
on the ibjjf site is yet. keep the number of batches reasonable, as you can get your IP blocked/banned if we abuse the 
number of calls

## Other Documentation Notes

- for each tournament, two files are produced. one file for the tournament results, and another for the registrations. the files are dumped in 'output/' and are prefixed with 'result' for results and 'registrations' for registrations. the tournament ID is also in the file name. Example:
```
output/result_345.txt
```

- to keep track of how many tournament id's have already been processed, we store them in a basic list in data/
- data/verified.txt keeps track of valid tournament id's that have resulted in a 200 success code. data/unverified.txt has tournament id's that returned an error code from the site
- many tournament id's are returning no data but 200 success. we will deal with this later
- referee seminars are getting their own tournament id

## future work

- we need better parsing of the results to categorize the referee seminars
- what will we do with failed calls? how do we further investigate bad id's?
