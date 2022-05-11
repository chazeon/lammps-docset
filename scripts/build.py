import re, sqlite3
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional

DOCSET_ROOT = 'lammps.docset'
DOCSET_DOCS = Path(f'{DOCSET_ROOT}/Contents/Resources/Documents')

class Docset():

    def __init__(self) -> None:
        self.conn = sqlite3.connect(f'{DOCSET_ROOT}/Contents/Resources/docSet.dsidx')
        self.cur = self.conn.cursor()

        try:
            self.cur.execute('DROP TABLE searchIndex;')
        except:
            pass

        self.cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
        self.cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
    
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def insert_index(self, name, type, path):
        self.cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, type, path))

    def find_by_name(self, name) -> list:
        self.cur.execute('SELECT * FROM searchIndex WHERE (name = ?)', (name,))
        return self.cur.fetchall()

    def find_by_path(self, path) -> list:
        self.cur.execute('SELECT * FROM searchIndex WHERE (path = ?)', (path,))
        return self.cur.fetchall()

def get_page_title(soup) -> Optional[str]:
    title = soup.find("title")
    return title.text
    
if __name__ == "__main__":

    docset = Docset()

    # Guide

    with open(DOCSET_DOCS / "Manual.html") as fp:
        soup = BeautifulSoup(fp, features="lxml")

    for a in soup.select("#user-guide a, #programmer-guide a"):
        res = re.search(r"^(\d+\.)+\s(.*)$", a.text)
        if res:
            name = res.group(2)
            path = a["href"]
            docset.insert_index(name, "Guide", path)
    
    # Commands

    for a in soup.select("#reference a"):
        if ".html" in a["href"]:
            with open(DOCSET_DOCS / a["href"]) as fp:
                soup2 = BeautifulSoup(fp, features="lxml")
                for a in soup2.select(".document li > a"):
                    name = re.sub("\s+command$", "", a.text)
                    path = a["href"]
                    docset.insert_index(name, "Command", path)

    # Programming API

    with open(DOCSET_DOCS / "genindex.html") as fp:
        soup = BeautifulSoup(fp, features="lxml")

    for a in soup.select(".document li > a"):
        res = re.search(r"^(.*)\s+\((.*\s+(\S+))\)$", a.text)
        if res:
            name = res.group(1)
            path = a["href"]
            type_ = res.group(3)
            docset.insert_index(name, type_.capitalize(), path)