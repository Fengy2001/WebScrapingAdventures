from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup



"""
initScrape Scrapes the HTML of the webpage, then invokes accessInnerHTML to 
obtain the innerHTML for beautifulsoup. Allowing access to the inner DOCTYPE.

Args:
    hyperlink: the link of the website

Returns:
    A beautiful soup object that contains the inner DOCTYPE
"""
def initScrape(hyperlink):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(hyperlink)
        page = accessInnerHTML(page)
        playwrightToStr = page.content
        htmlStr = playwrightToStr()
        webpage = BeautifulSoup(htmlStr, 'html.parser')
        browser.close()
        return webpage
    


"""
accessInnerHTML takes a playwright object and finds the iframe that contains the inner DOCTYPE
stored inside the current HTML.

Args:
    webpage: a playwright object

Returns:
    The inner HTML.
"""
def accessInnerHTML(webpage):
    innerHTML = webpage.wait_for_selector("iframe")
    innerHTML = innerHTML.content_frame()
    return innerHTML



"""
navToData prunes the unessecary HTML from the inner DOCTYPE, such that the
only the items in the listings remains.

Args:
    webpage: a beautifulSoup object

Returns:
    An array of listings in the form of beautifulsoup HTML.
"""
def navToData(webpage):
    dataSet = []
    for data in webpage.find_all("div", class_="col-12"):
        dataSet.append(data)
    return dataSet



"""
getTitle takes the navigated/pruned data and accesses the HTML tag that 
contains the title of each listing.

Args:
    data: pruned beautifulsoup objects

Returns:
    An array that contains the titles of each listing.
"""
def getTitle(data):
    titles = []
    for title in data:
        titleTag = title.find('h5', class_='ellipsis plugin-primary-color list-item-title')
        if titleTag is not None:
            listingTitle = titleTag.get_text(strip=True)
            titles.append(listingTitle)
    return titles



"""
getLink takes the navigated/pruned data and accesses the HTML tag that 
contains the hyperlink of each listing.

Args:
    data: pruned beautifulsoup objects

Returns:
    An array that contains the hyperlinks of each listing.
"""
def getLink(data):
    links = []
    for link in data:
        hyperlinkTag = link.find('a')
        if hyperlinkTag is not None:
            hyperlink = hyperlinkTag.get('href')
            links.append(hyperlink)
    return links



"""
hashData takes the arrays containing titles and links and combines them into a
hashtable allowing for access to hyperlinks by titles.

Args:
    titles: an array containing the titles of listings
    links:  an array containing the hyperlink of listings

Returns:
    A hashtable/dictionary containg the titles as keys and hyperlinks as values.
"""
def hashData(titles, links):
    if (len(titles) == len(links)):
        listingData = dict(zip(titles, links))
        return listingData
    else:
        return 0



"""
outputData takes a hashtables of listings and ouputs the title of the property aswell
as it's associated hyperlink.

Args:
    listings: a hashtable containing the titles as keys and hyperlinks as values.

Returns:
    Function does not return anything.
    However, the function generates a text file containing the ouputs.
"""
def outputData(listings):
    textFile = open('output.txt', 'w+')
    textFile.write('Avison Young data output: \n')
    for titles,links in listings.items():
        textFile.write("\n")
        textFile.write(titles + " : " + links)
        textFile.write("\n")
    textFile.close()



"""
The main function is responsible for controlling the majority of the other functions.
Allowing for quicker debugging and cleaner code.
"""
def main():
    webpage = initScrape('https://www.avisonyoung.ca/properties?saleOrLease=sale&propertyType=&searchText=calgary')
    data = navToData(webpage)
    listings = hashData(getTitle(data), getLink(data))
    outputData(listings)
    


"""
Call main.
"""
main()