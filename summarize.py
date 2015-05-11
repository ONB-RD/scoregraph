#!/usr/bin/env python
"""
Script for summarizing data for statistics generation.

Invocation:
$ python summarize.py data/enriched/*.json -o summary.csv
"""

import argparse
import csv
import json
import os
import sys


from common import write_json_file, progress, read_records


def summarize(data):
    
    artwork_links = 0
    if('sameas' in data):
        artwork_links = len(data['sameas'])

    persons = 0
    if('persons' in data):
        persons = len([person for person in data['persons']])

    links_person_gnd = 0
    links_person_dbpedia = 0
    links_person_viaf = 0
    if('persons' in data):
        for person in data['persons']:
            if('sameas' in person):
                links = [link for link in person['sameas']]
                links_person_gnd += len([link for link in links
                                        if 'gnd' in link])
                links_person_dbpedia += len([link for link in links
                                        if 'dbpedia' in link])
                links_person_viaf += len([link for link in links
                                        if 'viaf' in link])

    related_europeana_items = 0
    if('related_europeana_items' in data):
        related_europeana_items = len(data['related_europeana_items'])

    entry = {
        'id': data['aleph_id'],
        'links_artwork': artwork_links,
        'persons': persons,
        'links_person_gnd': links_person_gnd,
        'links_person_dbpedia': links_person_dbpedia,
        'links_person_viaf': links_person_viaf,
        'related_europeana_items': related_europeana_items
    }

    return entry


# Main summarization routine

def summarize_records(inputfiles, outputfile):
    print("Summarizing", len(inputfiles), "records in", outputfile)
    with open(outputfile, 'w') as csvfile:
        fieldnames = ['id',
                      'links_artwork',
                      'persons',
                      'links_person_gnd',
                      'links_person_dbpedia',
                      'links_person_viaf',
                      'related_europeana_items']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for filename, record in read_records(inputfiles):
            data = json.loads(record)
            entry = summarize(data)
            writer.writerow(entry)

# Command line parsing

parser = argparse.ArgumentParser(
                    description="Collecting data for dataset statistics.")
parser.add_argument('inputfiles', type=str, nargs='+',
                    help="Input files to be processed")
parser.add_argument('-o', '--outputfile', type=str, nargs='?',
                    default="data/summary.csv",
                    help="Output file")


if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
summarize_records(args.inputfiles, args.outputfile)
