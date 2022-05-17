#!/usr/bin/python3

def print_line(line: str):
    lines = line.split(",")
    for elem in lines:
        print(elem)

def read_file():
    with open("numbers.txt") as file:
        for line in file.readlines():
            print_line(line.strip())

if __name__ == '__main__':
    read_file()