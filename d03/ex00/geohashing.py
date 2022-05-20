#!usr/bin/python3

import sys
from antigravity import geohash

def main(): 
    try:
        latitude = float(sys.argv[1])
    except:
        return print("The latitude argument must have the type FLOAT")
    try:
        longitude = float(sys.argv[2])
    except:
        return print("The longitude argument must have the type FLOAT")
    try:
        datedow = sys.argv[3].encode("utf-8")
    except:
        return print("The datedow argument must have the type STRING")
    geohash(latitude, longitude, datedow)

if __name__ == '__main__': 
    if len(sys.argv) != 4:
        print("Use: geohashing.py 'latitude' 'longitude' 'datedow'")
        exit()
    main()