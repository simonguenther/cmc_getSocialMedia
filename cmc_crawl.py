import urllib
import sys
import re
import json
import codecs
from bs4 import BeautifulSoup
from Helper import get_html
from crawlWebsite import Crawler

URL_cmc = "https://coinmarketcap.com/all/views/all/"
baseURL = "https://coinmarketcap.com"
number_of_coins = 1000

"""
    Limit determines how many coin-links are retrieved
    0 = all
    >0 = number of coins
"""
def get_all_coin_links(source, limit):
    allNames = {}
    soup = BeautifulSoup(source, "lxml")
    count = 1
    for results in soup.findAll("td", {"class":"no-wrap currency-name"}):
        if count <= limit or limit == 0:
            coinname = results.text.strip()
            allNames[coinname] = baseURL + results.a['href']
            count += 1
        else:
            break
    return allNames

"""
    Extracts Links to websites from profile
    Returns: dictionary of all [Coinname] = list of Website-Links
"""
def get_all_website_links_from_coinpage(content):
    allWebsiteLinks = {}
    for coin in content:
        print "Retrieving Website: " + coin
        html = get_html(content[coin])
        
        soup = BeautifulSoup(html, "lxml")
        pattern = re.compile("Website[\s0-9]*")
        allSites = []
        
        for results in soup.findAll("a"):
            # Regex should already get rid off widget match, but for some reason doesn't
            if re.match(pattern,results.text) and "Widgets" not in results.text:
                allSites.append(results["href"])

        allWebsiteLinks[coin] = allSites
    return allWebsiteLinks

"""
    Save Doctopmary to File

"""
def save_to_file(path, dump):
	with codecs.open(path,'w','utf-8') as f:
		f.write(json.dumps(dump, ensure_ascii= False, indent=2, encoding = "utf-8"))

html = get_html(URL_cmc)
coinlinks = get_all_coin_links(html,number_of_coins)
dict_links = get_all_website_links_from_coinpage(coinlinks)
save_to_file("coin_link_list.json", dict_links)
    




