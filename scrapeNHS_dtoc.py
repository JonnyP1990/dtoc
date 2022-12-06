# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:32:04 2022

@author: jep39
"""

### NHS Data Web Scraper: delayed transfers of care (DTOC)
import os

os.chdir(r"C:\Users\jep39\PostdocFiles\DTOC")
path = os.getcwd()

import requests
from bs4 import BeautifulSoup

# NHS pages to scrape for data
URLs = {
    "url2011": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/dtoc-data-2011-12/",
    "url2012": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/dtoc-data-2012-13/",
    "url2013": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2013-14/",
    "url2014": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2014-15/",
    "url2015": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2015-16/",
    "url2016": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/2016-17-data/",
    "url2017": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2017-18/",
    "url2018": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/statistical-work-areas-delayed-transfers-of-care-delayed-transfers-of-care-data-2018-19/",
    "url2019": "https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2019-20/",
}

# define functions
def getPageElems(URL):
    """Find link content on page."""
    pg = requests.get(URL)
    sp = BeautifulSoup(pg.content, "html.parser")
    pginfo = sp.find(id="main-content")
    elems = pginfo.find_all("a")
    return elems


def getLinks(elements):
    """Save relevant links as a list."""
    links = []
    for e in elements:
        if ".csv" in e["href"]:
            links.append(e["href"])
    links.reverse()
    return links


def saveLinkFiles(linkList, saveStr):
    """Follow links and download data files.
    Naming format = year_month_dtoc.
    """
    datanames = []
    y, m = 2011, 4
    for L in linkList:
        split = os.path.splitext(L)
        dataget = requests.get(L)
        datanames.append(str(y) + "_" + str(m) + "_" + saveStr + split[1])
        datafile = open(datanames[-1], "wb")
        datafile.write(dataget.content)
        datafile.close()
        m += 1
        if m == 13:
            m = 1
            y += 1
    return datanames


# access and save data files
years = [
    "url2011",
    "url2012",
    "url2013",
    "url2014",
    "url2015",
    "url2016",
    "url2017",
    "url2018",
    "url2019",
]
for y in years:
    elems = getPageElems(URLs[y])
    links = getLinks(elems)
    fnames = saveLinkFiles(links, "dtoc")
