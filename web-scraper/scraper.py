from bs4 import BeautifulSoup
import requests
import os
import time
from weasyprint import HTML

# get the first page of the tutorial section to be scraped
def get_page(page):
    global parent
    page_gotten = requests.get(page).content
    soup = BeautifulSoup(page_gotten, 'html.parser')
    parent = soup.find(id = 'main')
    return parent

# move to the next page of this section 
def get_next_page(parent):
    global page
    links = parent.find_all('a')
    new_url = links[1].get('href')
    page = f'https://www.w3schools.com/python/{new_url}'
    return page

# cut away unnecessary divs and other html elements in one fell swoop 
# by targeting the parent container of said elements
def remove_unwanted(parent):
    tag = parent.find_all(id = 'mainLeaderboard')
    for div in tag:
        div.decompose()
    div_links = parent.find_all(class_ = 'w3-clear nextprev')
    for item in div_links:
        item.decompose()
    new_html = parent
    html = str(new_html)
    return html
    
# url of the first page of the python tutorial section   
page = 'https://www.w3schools.com/python/python_intro.asp'

# create empty lists to hold scraped pages and actual pages of the pdf document
# to be printed out

documents = []

# loop through each page of the tutorial calling the already declared functions
# on them
while True:     
    parent = get_page(page)
    get_next_page(parent)
    html = remove_unwanted(parent)

    # create an html instance
    html_instance = HTML(string=html)
    
    # call weasyprint's render method on the html instance to obtain in 
    # return an instance of the Document class which is stored in the doc object
    doc = html_instance.render()
    
    # append every consecutive doc object to the documents list
    # that was created earlier.
    documents.append(doc)

    # print the url of the current page to the console, this is solely
    # for debugging and has no effect on the script
    print(page)
    
    # let the loop sleep for about 3secs before sending another request to
    # to the server, this helps to prevent overloading the server from our end 
    time.sleep(3)

    # end loop when you get to your desired end-page
    if page == 'https://www.w3schools.com/python/python_mysql_getstarted.asp':
        break


# your pages containing your desired tutorial content are placed in the all_pages list
all_pages = [p for doc in documents for p in doc.pages]

# your pages are then written on document pages and are printed out as a pdf document
documents[0].copy(all_pages).write_pdf('combined.pdf')