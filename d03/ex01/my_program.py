#!/usr/bin/env python3
from path import Path

def main():
    try:
        Path.makedirs("folder")
    except FileExistsError as e:
        print(e)
    Path.touch("folder/file")
    file = Path("folder/file")
    file.write_lines(["Hello", "World"])
    print(file.read_text().strip())

if __name__ == "__main__":
    main()
