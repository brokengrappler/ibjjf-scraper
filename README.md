# ibjjf-scraper

To start, run setup shell script

```
./setup.sh
```

Usage

positional arguments:
1. batch size
number of tournament id's to check

2. time between runs (in seconds)
number of seconds between execution of scraper

3. number of times to run

```
python3 ibjjf_scraper.py 100 3600 3
```

the script makes one request call per second. the batch size (first argument) determines how many calls in a row it will make for each run.
after finishing a batch, it will wait for the number of seconds defined by the second argument before it tries another batch.
the third argument determines how many runs the script will make.

the purpose of these arguments is to get around scraping call limits. we do not know what the limits for the number of calls
on the ibjjf site is yet. keep the number of batches reasonable, as you can get your IP blocked/banned if we abuse the 
number of calls


