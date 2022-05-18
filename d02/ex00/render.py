#!/usr/bin/python3
import os
import sys
import re
import settings

def main():
    if (len(sys.argv) != 2):
        print("Invalid number of arguments")
        return
    path = sys.argv[1]
    temp = re.compile(".*\.template").match(path)
    if not temp:
        print("Invalid file extension, use: .template")
        return
    if not os.path.isfile(path):
        print("The file named {} does not exist".format(path))
        return
    with open(path, 'r') as file:
        template = "".join(file.readlines())
    pattern = template.format(
        name=settings.name,
        surname=settings.surname,
        age=settings.age,
        prof=settings.prof,
        title=settings.title,
        minishell=settings.minishell,
        minirt=settings.minirt,
        cpp=settings.cpp,
        pushswap=settings.pushswap
    )
    name = os.path.splitext(path)[0]
    path = "".join(name + ".html")
    with open(path, 'w') as file:
        file.write(pattern)

if __name__ == '__main__':
    main()