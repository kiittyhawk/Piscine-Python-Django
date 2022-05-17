#!/usr/bin/python3
import sys

def state(capital: str):
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
    capital2 = capital
    for k, v in capital_cities.items():
        if v == capital:
            capital = k
    if capital == capital2:
        print("Unknown state")
        return
    for k, v in states.items():
        if v == capital:
            print(k)

def main():
    if len(sys.argv) == 2:
        state(sys.argv[1])

if __name__ == '__main__':
    main()
