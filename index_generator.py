# assumes that TITLE_LOCATOR is always the line before the actual title
# find all instances of TITLE_LOCATOR in articles directory and store next line

import os
import pathlib
import re
from datetime import datetime


FOLDER_NAME = "articles"
ARTICLE_PATH = pathlib.Path(__file__).parent / FOLDER_NAME

DIR_LIST = os.listdir(ARTICLE_PATH)

TITLE_LOCATOR = "<div class=\"articles\">"


def count_articles():
    article_count = 0
    for article in DIR_LIST:
        article_count += 1
    print("Found", article_count, "articles")

    return article_count


def file_names():
    file = []
    for article in DIR_LIST:
        file.append(article)

    return file


def parse_titles():
    all_lines = []
    title_lines = []
    locator_iterator = 0

    for article in DIR_LIST:                                            # get lines of all articles
        with open(str(ARTICLE_PATH) + "\" + article, 'rt') as file:
            for line in file:
                all_lines.append(line)
            file.close()

    for line in all_lines:                                              # store next line after locator is found
        if TITLE_LOCATOR in line:
            title_lines.append(all_lines[locator_iterator+1])
        locator_iterator += 1

    return title_lines


def remove_tags():
    title_lines = parse_titles()
    tags_removed_titles = []

    for title in title_lines:
        pattern = re.compile("(<p>|</p>)", re.I)
        tags_removed_titles.append(pattern.sub("", title))

    return tags_removed_titles


def add_links():
    title_lines = remove_tags()
    links = file_names()
    link_iterator = 0
    links_added_titles = []

    link_builder_close = "</a>"
    link_locator_open = "</span>"
    link_locator_close = "<br>"

    for title in title_lines:
        link_builder_open = "<a href=\"articles/" + links[link_iterator] + "\">"
        link_builder_open_pattern = re.compile(link_locator_open, re.I)
        link_builder_string = (link_builder_open_pattern.sub(link_locator_open+link_builder_open, title))
        
        link_builder_close_pattern = re.compile(link_locator_close, re.I)
        link_builder_string = (link_builder_close_pattern.sub(link_builder_close+link_locator_close, link_builder_string))

        links_added_titles.append(link_builder_string)
        link_iterator += 1

    links_added_titles = ["<!--generated-->" + item for item in links_added_titles]
    return links_added_titles


def sort_links():
    sort_list = add_links()

    sort_list = sorted(
        sort_list,
        key=lambda x: datetime.strptime(x[43:55], '[%d-%m-%Y]'))  # very dependent on doc format

    return sort_list


def write_index():
    write_list = sort_links()
    print(os.listdir())
    with open("index.html", 'r') as file:
        lines = file.readlines()
        file.close()

    with open("index.html", 'w') as file:
        for i in range(0, len(lines)):
            if not "<!--generated-->" in lines[i]:
                file.write(lines[i])
        file.close()

    with open("index.html", 'r') as file:
        lines = file.readlines()


    with open("index.html", 'w') as file:
        for i in range(0, len(lines)):

            if "<!--articles begin-->" in lines[i]:

                for a in range(0, len(write_list)):
                    lines.insert(i+1, write_list[a])
                    print(write_list[a])

        for i in range(0, len(lines)):
            file.write(lines[i])


def main():
    write_index()

main()

