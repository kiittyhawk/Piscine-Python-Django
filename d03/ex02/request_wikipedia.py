#!/usr/bin/venv python3

import requests
import json
import dewiki
import sys

def req_wiki(page: str):
    url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "format": "json",
        "redirects": "true",
        "formatversion": 2
    }

    res = requests.get(url=url, params=params)
    try:
        res.raise_for_status()
    except requests.HTTPError as e:
        return print("Error loading the page: {err}".format(err=str(e)))
    try:
        data = json.loads(res.text)
    except requests.JSONDecodeError as e:
        return print("Deserialization error: {err}".format(err=e))
    try:
        data = dewiki.from_string(data["parse"]["wikitext"]).replace("\n\n", "\n")
    except Exception as e:
        return print("Undefined behavior: {err}".format(err=e))
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid number of arguments: {}".format(len(sys.argv) - 1))
        exit()
    data = req_wiki(sys.argv[1])
    if not data:
        exit()
    try:
        with open("{}.wiki".format(sys.argv[1]), "w") as file:
            file.write(data)
    except Exception as e:
        print(e)
        exit()
    