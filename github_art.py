#!/usr/bin/env python3

import os
import sys
import time
import datetime
import calendar
from PIL import Image as pillow

def print_help(exec: str, status: int):
    print(f"Usage : {exec} <image> <repository-dir> <username> <email> <year>")
    sys.exit(status)

def first_january_weekday(year: int) -> int:
    date = datetime.date(year, 1, 1)

    return (date.weekday() + 1) % 7

def number_of_days(year: int) -> int:
    return 366 if calendar.isleap(year) else 365

def get_nth_day(year: int, n: int) -> datetime.date:
    return datetime.date(year, 1, 1) + datetime.timedelta(days=n)

def main():
    args: list = sys.argv

    if len(args) == 2 and args[1] in ["-h", "--help"]:
        print_help(args[0], 1)

    if len(args) != 6:
        print_help(args[0], 1)

    image_path: str = args[1]
    repo_path: str = args[2]
    username: str = args[3]
    email: str = args[4]
    year: str = args[5]

    try:
        img: pillow.Image = pillow.open(image_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    color_palette: list = ["161b22", "0e4429", "006d32", "26a641", "39d353"]
    to_int: dict = {color: i for i, color in enumerate(color_palette)}

    commits_per_day = [[0 for _ in range(img.width)] for _ in range(img.height)]

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, *_ = img.getpixel((x, y))

            if f"{r:02x}{g:02x}{b:02x}" not in color_palette:
                exit(f"Error: Image contains color not in palette: {r:02x}{g:02x}{b:02x}")

            commits_per_day[y][x] = to_int[f"{r:02x}{g:02x}{b:02x}"]

    os.chdir(repo_path)
    # file = open("file.txt", "w")

    y: int = first_january_weekday(int(year))
    x: int = 0

    for n in range(number_of_days(int(year))):
        date = get_nth_day(int(year), n)
        date_time = f"{date} 12:00:00"
        date__time_formated = f"{date}T12:00:00"


        for i in range(commits_per_day[y][x]):
            # Write line to file
            os.system(f"echo 'github_art commit' >> file.txt")
            # Add change
            os.system(f"git add file.txt")
            # Commit change
            os.system(f'GIT_COMMITTER_DATE="{date_time}" git commit --date="{date__time_formated}" -m "github_art commit" --author="{username} <{email}>"')
        y += 1
        if y == 7:
            y = 0
            x += 1

    os.system("git push")
if __name__ == "__main__":
    main()