#!/usr/bin/env python
"""
Script for extracting relevant data points from raw data.

Invocation:
$ python normalize.py
"""
import os
import json
from bs4 import BeautifulSoup

RAW_DATA_DIR = "data/raw"
NORMALIZED_DATA_DIR = "data/normalized"

GND_PREFIX = "http://d-nb.info/gnd"


def find_tags_in_id_range(soup, start, end):
    tags = [tag for tag in soup.find_all("varfield")
            if tag['id'] and tag['id'].isnumeric() and
            int(tag['id']) >= start and int(tag['id']) < end]
    return tags


def persons(soup):
    persons = []
    tags = find_tags_in_id_range(soup, 100, 200)
    for tag in tags:
        # name
        name = tag.find(label="p")
        if not name:
            name = tag.find(label="a")
        if name:
            name = name.string
        # lifetime
        lifetime = tag.find(label="d")
        if lifetime:
            lifetime = lifetime.string
        # gnd_link
        gnd_link = tag.find(label="9")
        if gnd_link:
            gnd_link = GND_PREFIX + "/" + gnd_link.string[8:]
        # role
        role = tag.find(label="b")
        if role:
            role = role.string.replace("[", "").replace("]", "")
        person = {
            'name': name,
            'lifetime': lifetime,
            'role': role,
            'gnd_uri': gnd_link
        }
        persons.append(person)
    return persons


def content(soup):
    contents = []
    for tag in soup.find_all("varfield", id="655"):
        uri = tag.find("subfield", label="u")
        note = tag.find("subfield", label="z")
        if uri:
            content = {
                'uri': uri.string,
                'note': note.string
            }
            contents.append(content)
    return contents


def title(soup):
    tag = soup.find("varfield", id="303")
    if not tag:
        return None
    else:
        title = tag.find("subfield", label="t")
        if not title:
            return None
        else:
            return title.string


def subtitles(soup):
    subtitles = []
    tags = find_tags_in_id_range(soup, 304, 400)
    for tag in tags:
        subfields = tag.find_all("subfield")
        for subfield in subfields:
            contents = subfield.string.replace("[", "").replace("]", "")
            subtitles.append(contents)
    return subtitles


def dates(soup):
    dates = []
    date_tags = soup.find_all("varfield", id="425")
    for tag in date_tags:
        dates.append(tag.subfield.string)
    return dates


def gnd_link(soup):
    tag = soup.find("varfield", id="303")
    if not tag:
        return None
    else:
        gnd_link = tag.find("subfield", label="9")
        if not gnd_link:
            return None
        else:
            return GND_PREFIX + "/" + gnd_link.string[8:]


def notes(soup):
    notes = []
    tags = find_tags_in_id_range(soup, 400, 600)
    for tag in tags:
        if tag.id != "425":
            for subfield in tag.find_all("subfield", label="a"):
                notes.append(subfield.string)
    return notes


def terms(soup):
    terms = []
    tags = find_tags_in_id_range(soup, 900, 1000)
    for tag in tags:
        labels = []
        for subfield in tag.find_all("subfield"):
            if subfield["label"] != "9":
                labels.append(subfield.string)
        gnd_link = tag.find("subfield", label="9")
        if gnd_link:
            gnd_link = GND_PREFIX + "/" + gnd_link.string[8:]
        term = {'labels': labels, 'gnd_link': gnd_link}
        terms.append(term)
    return terms


def doc_id(soup):
    return soup.doc_number.string


def convert_to_json(xml_file):
    with open(xml_file, 'r') as in_file:
        soup = BeautifulSoup(in_file)
        output = {
            'id': doc_id(soup),
            'title': title(soup),
            'subtitles': subtitles(soup),
            'persons': persons(soup),
            'content': content(soup),
            'dates': dates(soup),
            'gnd_uri': gnd_link(soup),
            'notes': notes(soup),
            'terms': terms(soup)
        }
        return output


def main():
    for f in os.listdir(RAW_DATA_DIR):
        output = convert_to_json(RAW_DATA_DIR + '/' + f)
        outfile = f.replace("xml", "json")
        with open(NORMALIZED_DATA_DIR + "/" + outfile, "w") as out_file:
            json.dump(output, out_file, sort_keys=True, indent=4,
                      ensure_ascii=False)

if __name__ == "__main__":
    main()
