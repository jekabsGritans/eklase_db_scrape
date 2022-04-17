import lxml.html, re
from base.target import Target
from collections import namedtuple
from datetime import date, timedelta
import pandas as pd
import numpy as np
from base.db import default_db, Table
from base.scraper import SecretScraper

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) // 7):
        yield start_date + timedelta(7*n)


subjects = {
    "Matemātika": "math",
    "Angļu": "eng",
    "Latviešu": "lat",
    "Franču": "fr",
    "Zināšanu": "tok",
    "Programmēšana": "compsci",
    "Matemātiskā": "calc",
    "Literatūra": "lit",
    "Sports": "pe",
    "Fizika": "phy",
    "Vēsture": "hist",
    "Ekonomika": "econ"
}

class Eklase(Target):
    Model = namedtuple("lessons","school_date, subject, topic, homework")

    def __init__(self, start_date, end_date):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
    
    def urls(self):
        start_date = self.start_date
        end_date = self.end_date
        for day in daterange(start_date,end_date):
            url = day.strftime("https://my.e-klase.lv/Family/Diary?Date=%d.%m.%Y.")
            yield url

    def extract_items(self, response):
        items = [] 
        parser = lxml.html.HTMLParser(encoding="utf-8")
        doc = lxml.html.fromstring(response.content, parser=parser)
        date_heads = doc.xpath("//div[@class='student-journal-lessons-table-holder hidden-xs']/h2")
        tables = doc.xpath("//div[@class='student-journal-lessons-table-holder hidden-xs']/table[@class='lessons-table']")
        for date_head, table in zip(date_heads,tables):
            try:
                df = pd.read_html(lxml.html.tostring(table))[0]
                df.drop(df.columns[-1], axis=1, inplace=True)
                df.columns = "subject topic homework".split()
                df = df.replace({np.nan: None})
                df.subject = df.subject.map(lambda x: x.replace("  "," ").split(" ")[1])
                df.subject = df.subject.map(lambda x: subjects[x])
                date_comps = date_head.text.split(".")
                d = date(2000+int(date_comps[2]),int(date_comps[1]),int(date_comps[0]))
                for row in df.itertuples():
                    items.append(self.Model(school_date=d, subject=row.subject, topic=row.topic, homework=row.homework))
            except:
                pass
        return items, []


eklase = Eklase(date(2021,9,1), date(2022,4,17))

table = Table(default_db, eklase.Model)
scraper = SecretScraper(eklase, table)

from creds import username, password
scraper.user.post("https://my.e-klase.lv/?v=15", data={"fake_pass":"","UserName":username,"Password":password})
scraper.start()