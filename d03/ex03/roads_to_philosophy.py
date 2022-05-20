#!/usr/bin/venv python3
import sys
from bs4 import BeautifulSoup
import requests

class roads_to_philosophy:
    def __init__(self) -> None:
        self.road = []

    def search_wiki(self, page:str):
        
        url = "https://en.wikipedia.org{page}".format(page=page)

        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 404:
                return print("It's a dead end !")
            return print(e)
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find(id="firstHeading").text
        if title in self.road:
            return print("It leads to an infinite loop !")
        self.road.append(title)
        print(title)
        if title == "Philosophy":
            return print("{number} roads from {request} to philosophy".format(number=len(self.road), request=self.road[0]))
        content = soup.find(id='mw-content-text')
        links = content.select('p > a')
        for link in links:
            if link.get('href') is not None and link['href'].startswith('/wiki/')\
                        and not link['href'].startswith('/wiki/Wikipedia:') and not link['href'].startswith('/wiki/Help:'):
                return self.search_wiki(link['href'])
        return print("It leads to a dead end !.")
        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        wiki = roads_to_philosophy()
        wiki.search_wiki("/wiki/{}".format(sys.argv[1]))
    else:
        print("Invalid number of arguments: {}".format(len(sys.argv) - 1))
        exit()
