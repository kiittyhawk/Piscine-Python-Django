#!/usr/bin/python3
import sys

def get_v(d: dict, s: str):
    for k, v in d.items():
        if k.lower() == s.lower():
            return v
    return None

def get_k(d: dict, s: str):
    for k, v in d.items():
        if v.lower() == s.lower():
            return k
    return None

def all_in(value: str):
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
    v = get_v(states, value)
    k = get_k(capital_cities, value)
    if v:
        print(capital_cities.get(v), "is the capital of " + get_k(states, v))
    elif k:
        print(capital_cities.get(k), "is the capital of " + get_k(states, k))
    else:
        print(value + " is neither a capital city nor a state")

def main():
    if len(sys.argv) != 2:
        return
    args = sys.argv[1].split(',')
    for arg in args:
        arg = arg.strip()
        if arg == '':
            continue
        all_in(arg)

if __name__ == '__main__':
    main()
