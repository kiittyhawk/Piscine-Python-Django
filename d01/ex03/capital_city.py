#!/usr/bin/python3
import sys

def capital_city(state: str):
    states = {
    "Oregon" : "OR",
    "Alabama" : "AL",
    "New Jersey": "NJ",
    "Colorado" : "CO"
    }
    capital_cities = {
    "OR": "Salem",
    "AL": "Montgomery",
    "NJ": "Trenton",
    "CO": "Denver"
    }
    state = states.get(state)
    if not state:
        print("Unknown state")
        return
    print(capital_cities.get(state))

def main():
    if (len(sys.argv) == 2):
        capital_city(sys.argv[1])

if __name__ == '__main__':
    main()
