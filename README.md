# scoregraph

A collection of scripts for transforming ONB music score metadata into a semantically enriched knowledge graph of music scores.

## Data aggregation

Starting from the ONB's raw music score dataset (Aleph export) data aggregation involves the following steps:

+ Data normalization: transform raw aleph data to JSON and extract relevant data fields
+ Data enrichment:
    + follow GND links in raw/normalized data and collect additional uris (e.g., DBpedia, VIAF)
    + find related Europeana items by (i) searching via the Europeana search API and (ii) filtering those that share at least one URI with the raw/normalized data


## Script usage

Preconditions: Python 3.4.0 or greater installed

Install dependencies:

    pip install -r requirements.txt


Enable script execution

    chmod u+x *.py


Run data normalization script

    ./normalize -o data/normalized data/raw/*.xml


Run data enrichment script

    ./enrich -o data/enriched -e YOUR_EUROPEANA_API_KEY data/normalized/*.json
