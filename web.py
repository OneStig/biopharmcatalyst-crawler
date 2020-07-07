# selenium, bs4, lxml, json
# https://sites.google.com/a/chromium.org/chromedriver/downloads

from selenium import webdriver
from bs4 import BeautifulSoup
import json

class Drug:
    def __init__(self, name, indication, stage, newstxt, newslink):
        self.name = name
        self.indication = indication
        self.stage = stage
        self.newstxt = newstxt
        self.newslink = newslink

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

options = webdriver.ChromeOptions()

driver = webdriver.Chrome("C:/Windows/chromedriver.exe", chrome_options=options)

driver.get('https://www.biopharmcatalyst.com/biotech-stocks/company-pipeline-database')

soup = BeautifulSoup(driver.page_source, "lxml")

companydiv = soup.findAll("div", {"class": "filter-table__row js-tr"})

companydrugs = dict()

for company in companydiv:

    inner = BeautifulSoup(company.encode_contents(), "lxml")
    companyname = inner.findAll("a", {"class": "company-name"})[0].get_text()

    drugs = []

    trs = inner.findAll("tr", {"class": "js-drug js-td--fda js-td--portfolio"})

    for items in trs:
        itemdata = BeautifulSoup(items.encode_contents(), "lxml")

        properties = itemdata.findAll("td")

        c = 0

        name = ""
        ind = ""
        stage = items['data-value']
        news = ""
        link = ""
        
        for prop in properties:
            ptext = prop.get_text().encode("utf-8")
            if c == 0:
                name = ptext
            elif c == 1:
                ind = ptext
            else:
                break

            c += 1

        try:
            t = itemdata.findAll('a')[0]
            link = t['href']
            news = t.get_text()
        except:
            link = "#"
            news = "None"
        

        addeddrug = Drug(name, ind, stage, news, link)

        drugs.append(addeddrug)

    companydrugs[companyname] = drugs

# data = json.dumps(companydrugs, default=dumper, indent=2, ensure_ascii=False)

with open('output.json', 'w') as outf:
    json.dump(companydrugs, outf, default=dumper, indent=2, ensure_ascii=False)