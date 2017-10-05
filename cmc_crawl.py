import urllib
import sys
import re
from bs4 import BeautifulSoup

URL_cmc = "https://coinmarketcap.com/all/views/all/"
baseURL = "https://coinmarketcap.com"

"""
    get HTML from link
"""
def get_html(url):
    try:
        return urllib.urlopen(url).read()
    except:
        print("Error", sys.exc_info()[0])
        raise

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


html = get_html(URL_cmc)
coinlinks = get_all_coin_links(html,3)
get_all_website_links_from_coinpage(coinlinks)




