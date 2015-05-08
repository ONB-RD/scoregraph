#!/usr/bin/env python
"""
Script for enriching normalized data with contextually relevant data.

Invocation:
$ python enrich.py -a EUROPEANA_API_KEY
"""

import os
import glob
import requests
import json

EUROPEANA_API_KEY = "XtMoz8MgC"
EUROPEANA_API_URI = "http://europeana.eu/api/v2/search.json?"
EUROPEANA_MAX_ROWS = 20

NORMALIZED_DATA_FILES = "data/normalized/*.json"
ENRICHED_DATA_DIR = "data/enriched"


def find_europeana_items(query):
    print("Searching Europeana items matching:", query, "...")

    payload = {'wskey': EUROPEANA_API_KEY,
               'profile': 'standard',
               'query': query,
               'start': 1,
               'rows': EUROPEANA_MAX_ROWS}
    r = requests.get(EUROPEANA_API_URI, params=payload)
    result = r.json()
    items = result['items']
    print("Found", len(items), "items.")
    return items


def extract_europeana_data(europeana_items):
    data = []
    for item in europeana_items:
        data.append({'id': item.get('id'),
                     'creator': item.get('dcCreator'),
                     'title': item.get('title'),
                     'score': item.get('score')})
    return data


def filter_europeana_items(data, europeana_items):
    # keep only those items that have a matching author (by uri)
    person_uris = [person['gnd_uri'] for person in data['persons']]
    print(person_uris)
    filtered_items = []
    for item in europeana_items:
        if item.get('dcCreator'):
            for term in item['dcCreator']:
                if term in person_uris:
                    filtered_items.append(item)
    return filtered_items


def enrich_europeana(data):
    """Enriches a normalized record with Europeana data"""
    title = data['title']
    for person in data['persons']:
        name = person['name']
        query = name if name else "" + title if title else ""

        # all items returned by Europeana
        europeana_items = find_europeana_items(query)
        # filter items
        europeana_items = filter_europeana_items(data, europeana_items)
        # extract enrichments
        enrichments = extract_europeana_data(europeana_items)

        if data.get('related_europeana_items') is not None:
            data['related_europeana_items'].extend(enrichments)
        else:
            data['related_europeana_items'] = enrichments
    return data


# I/O handling
def normalized_files():
    norm_files = glob.glob(NORMALIZED_DATA_FILES)
    for norm_file in norm_files:
        with open(norm_file, 'r') as in_file:
            data = json.load(in_file)
            yield (norm_file, data)


def write_json_file(dir, filename, data):
    with open(dir + "/" + filename, "w") as out_file:
            json.dump(data, out_file, sort_keys=True, indent=4,
                      ensure_ascii=False)


def main():
    for norm_file, data in normalized_files():
        print("Enriching", norm_file, "...")
        enriched_data = enrich_europeana(data)
        filename = os.path.basename(norm_file).replace(".json",
                                                       "_enriched.json")
        write_json_file(ENRICHED_DATA_DIR, filename, enriched_data)

if __name__ == "__main__":
    main()

