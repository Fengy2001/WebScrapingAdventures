from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup



def initScrape(hyperlink):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(hyperlink)
        playwrightToStr = page.content
        htmlStr = playwrightToStr()
        webpage = BeautifulSoup(htmlStr, 'html.parser')
        browser.close()
        return webpage


"""
Issue is currently with this method, the method currently returns nothing. 
Which is strange since my html says that the data should all be contained in this div class.
"""
def navToData(webpage):
    dataSet = []
    for data in webpage.find_all("div", class_="js-listing-container py-2"):
        print("wow!")
        dataSet.append(data)
    return dataSet



def getTitle(data):
    pass



def getLink(data):
    dataSet = []
    for data in data.find_all('a'):
        dataSet.append(data)
    return dataSet



def main():
    webpage = initScrape('https://www.avisonyoung.ca/properties?saleOrLease=sale&propertyType=&searchText=calgary')
    data = navToData(webpage)
    print(data)
    #links = getLink(data)
    #print(len(links))


main()