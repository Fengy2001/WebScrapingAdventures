from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup



"""
Initial scraping begins, using playwright, the webpage is opened.
Once opened the accessInnerHTML function is called to access the inner DOCTYPE.
Once obtained, beautiful soup scrapes the innerHTML and allowing for data scraping to begin.
The function then returns the beautifulsoup Object.
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
accessInnerHTML is a function that takes one input of the form of a playwright object. It navigates
to the DOCTYPE nested inside the outer html and returns the whole inner HTML as a playwright object.
"""
def accessInnerHTML(webpage):
    innerHTML = webpage.wait_for_selector("iframe")
    innerHTML = innerHTML.content_frame()
    return innerHTML



"""
Issue is currently with this method, the method currently returns nothing. 
Which is strange since my html says that the data should all be contained in this div class.
"""
def navToData(webpage):
    dataSet = []
    for data in webpage.find_all("div", class_="col-12"):
        dataSet.append(data)
    return dataSet



"""
This function takes one input and is in the form of a navigated soup object.
The function then looks through all the navigated objects and looks for a h5 tag which contains
the title of the property. These are then scraped and the results are returned in the form of an array.
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
The getLink function takes the input in the form of a navigated soup object.
The function then looks through all the navigated objects and looks for a tags. 
Once found the hyperlink is extracted and stored into an array.
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
This function takes two inputs both of type arrays.
Hash data takes the titles and links scraped from the website and 
associates them together such that they can be accessed by link or by title.
"""
def hashData(titles, links):
    if (len(titles) == len(links)):
        listingData = dict(zip(titles, links))
        return listingData
    else:
        return 0



"""
This function takes a hashtable/dictionary and outputs them as a text file.
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