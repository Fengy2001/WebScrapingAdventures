from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup



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



def getTitle(data):
    pass



def getLink(data):
    links = []
    for link in data:
        hyperlink = link.find('a')
        if hyperlink is not None:
            links.append(hyperlink)
            print(hyperlink.get('href'))
    return links



def main():
    webpage = initScrape('https://www.avisonyoung.ca/properties?saleOrLease=sale&propertyType=&searchText=calgary')
    data = navToData(webpage)
    links = getLink(data)


main()