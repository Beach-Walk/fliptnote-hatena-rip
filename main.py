import time
from bs4 import BeautifulSoup
import requests
import re

#base url of website
url_base = "https://archive.sudomemo.net"
# profile page # API trunkated (to be appended later)
# NOT AFFILIATED WITH USER. ONLY AN EXAMPLE
url_profile = "/user/0022D670AA386C3B@DSi?page="
#add url base  + url profile
url_crafted = url_base+url_profile
urls_pages = []
urls_pages_parsed= []
urls_vid_pages = []
urls_vid_pages_parsed = []
urls_download = []


pages = int(input("How many pages are on your profile?\n"))#5
x=1
while x <=pages:
    urls_pages.append(url_crafted + str(x))
    x=x+1

print(urls_pages)

for url in urls_pages:
    url_raw = requests.get(url)
    soup = BeautifulSoup(url_raw.text, "html.parser")
    urls_pages_parsed.append(soup)
#inter through parsed list
count_cur_page = 1
for pu in urls_pages_parsed:

    count_filtered_urls = 0 #stats for # of urls filterd
    #find all href links on page
    for au in pu.find_all('a',href=True):
        cur_url = au.get('href')
        #filter out the urls for the one we want
        if "/watch/" in cur_url:
            #add to list and prepend the base url so we can vist the page later
            urls_vid_pages.append(url_base+cur_url)
            count_filtered_urls = count_filtered_urls + 1 #count for stats
    print("Page " + str(count_cur_page) +" found " + str(count_filtered_urls) + " filtered URLs")
    count_cur_page = count_cur_page + 1

print("Total filtered URLs: "+str(len(urls_vid_pages)))
#
#We now have a list of pages we must visit to download the flipnotes
#Next wee need to vist the pages and extract the resource that contains the file URL
#

print("Parsing video pages (this may take a while)...", end="")

for url in urls_vid_pages:
    url_raw = requests.get(url)
    soup = BeautifulSoup(url_raw.text, "html.parser")
    urls_vid_pages_parsed.append(soup)
    print(".",end="")

print("DONE!")

print("Finding and filtering URLs")
cur_download_i = 0
for pu in urls_vid_pages_parsed:

    count_filtered_urls = 0  # stats for # of urls filterd
    # find all href links on page
    for au in pu.find_all('flipnote-player', src=True):
        cur_url = au.get('src')
        # filter out the urls for the one we want
        if "/theatre_assets/images/dynamic/movie/" in cur_url:
            # add to list and prepend the base url so we can vist the page later
            urls_download.append(url_base + cur_url)
            count_filtered_urls = count_filtered_urls + 1  # count for stats
    print("Page: " + urls_vid_pages[cur_download_i] + " found " + str(count_filtered_urls) + " resource to DL")
    cur_download_i = cur_download_i +1

#print(urls_download)

#download all URLs
for ud in urls_download:
    time.sleep(0.2)
    fm_regex = ".*\/theatre_assets\/images\/dynamic\/movie\/(?P<filename>\w*$|.*(?=\?))"
    filename = re.search(fm_regex,str(ud)).group("filename")
    filename_w_ext = filename + ".ppm"
    response = requests.get(ud)
    print("Saving 'flipnotes/"+filename_w_ext+"'")
    open("flipnotes/"+filename_w_ext, "wb").write(response.content)

print("Done!")

