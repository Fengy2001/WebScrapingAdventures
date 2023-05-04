import requests
from bs4 import BeautifulSoup

# https://finance.yahoo.com/quote/GME/key-statistics?p=GME

"""
Variable headers is used for userAgent such that the website is accessible.
"""
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}



"""
Starts the scraping proccess.
only input is the link you want to scrape.
"""
def initScrape(hyperlink):
    response = requests.get(hyperlink, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')



"""
Function that uses a crude non-adaptive method to access data from tables. Only works for yahoo keystatistic websites.
Takes the input of a
    - beautifulsoup object parsed with html.parser
"""
def yahooFinanceNav(webpage):
    tables = []
    for table in webpage.find_all("table", class_="W(100%) Bdcl(c)"):
        if table.parent.name == "div":
            tables.append(table)
    return tables



"""
Puts Data from tables into a hashtable/dictionary so that it is directly accessible by iterate or name.
Takes an input of a list that consists of html table elements.

Removable sections are any lines of code that use the variable "i". This was introduced since my objective was to
only output the 2nd row of data from each table. Otherwise this function will return a hashtable that contains the data
of all tables.
"""
def hashData(tables):
    data = {}
    for table in tables:
        i = 0
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                data[label] = (value)
            if i == 1:
                print(label, value)
            i += 1
    return data



"""
Main function for easier accesiability to functions.
Main end with a dictionary/hashtable that contains the data of the tables.
Thus, allowing for easy access to data.
"""
def main():
    websiteLink = "https://finance.yahoo.com/quote/GME/key-statistics?p=GME" #str(input("Paste the link: "))
    webpage = initScrape(websiteLink)
    tables = yahooFinanceNav(webpage)
    data = hashData(tables)


    
"""
Call main method.
"""
main()
