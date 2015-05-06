#!/usr/bin/env python
"""
Script for summarizing data for statistics generation.

Invocation:
$ normalize.py
"""

import glob
import json
import csv
import os

NORMALIZED_DATA_FILES = "data/normalized/*.json"
SUMMARY_FILE = "summary.csv"


def summarize(data):
    persons = data['persons']
    persons_linked = [person for person in persons if person['gnd_uri']]
    artwork_links = data['gnd_uri']
    if artwork_links:
        no_artwork_links = 1
    else:
        no_artwork_links = 0

    entry = {
        'no_person': len(persons),
        'no_person_links': len(persons_linked),
        'no_artwork_links': no_artwork_links
    }

    return entry


def main():
    files = glob.glob(NORMALIZED_DATA_FILES)
    with open(SUMMARY_FILE, 'w') as csvfile:
        fieldnames = ['id',
                      'no_person',
                      'no_person_links',
                      'no_artwork_links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for f in files:
            with open(f, "r") as in_file:
                data = json.load(in_file)
                entry = summarize(data)
                entry['id'] = os.path.basename(f)[:-5]
                writer.writerow(entry)

if __name__ == "__main__":
    main()
