import requests
from bs4 import BeautifulSoup


"""
Variable headers is used for userAgent such that the website is accessible.
"""
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}



"""
initScrape starts the scraping proccess.

Args:
    hyperlink:  The link of the website you want to scrape

Returns:
    A html beautifulSoup object.
"""
def initScrape(hyperlink):
    response = requests.get(hyperlink, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')



"""
yahooFinance is a function that prunes the unwanted HTML such that only the data
that's of interest remains as in the beautifulsoup object.

Args:
    webpage:    A html beautifulsoup object

Returns:
    A list of html beautifulsoup objects that contain the data of each separate table.
"""
def yahooFinanceNav(webpage):
    tables = []
    for table in webpage.find_all("table", class_="W(100%) Bdcl(c)"):
        if table.parent.name == "div":
            tables.append(table)
    return tables



"""
hashData takes Data from tables and associates them to a hashtable/dictionary so that it is
accessible by name or iterate.

Args:
    tables: A list of beautifulsoup objects that only contain the html of each table

Returns:
    A hashtable/dictionary containing the label of the data and the data.

Removable sections are any lines of code that use the variable "i". This was introduced since 
my objective was to only output the 2nd row of data from each table. Otherwise this function 
will return a hashtable that contains the data of all tables.
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
"""
def main():
    websiteLink = "https://finance.yahoo.com/quote/GME/key-statistics?p=GME"
    webpage = initScrape(websiteLink)
    tables = yahooFinanceNav(webpage)
    data = hashData(tables)


    
"""
Call main method.
"""
main()
