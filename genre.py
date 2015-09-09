#!/usr/bin/env python
"""
Script for finding GND reference used for genre classification.

Invocation:
$ python genre.py data/enriched/*.json
"""

import argparse
import json
import os
import sys

from common import read_records

uris = []

def summarize(data):
    if('genres' in data):
        for genre in data['genres']:
            if('sameas' in genre):
                for uri in genre['sameas']:
                    uris.append(uri)

# Main summarization routine

def summarize_records(inputfiles):
    for filename, record in read_records(inputfiles):
        data = json.loads(record)
        summarize(data)
    uris_unique = sorted(set(uris))
    print(len(uris_unique), " different GND references:")
    for uri in uris_unique:
        print(uri)

# Command line parsing

parser = argparse.ArgumentParser(
                    description="Collecting data for dataset statistics.")
parser.add_argument('inputfiles', type=str, nargs='+',
                    help="Input files to be processed")

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
summarize_records(args.inputfiles)
