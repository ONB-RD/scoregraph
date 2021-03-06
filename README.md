# scoregraph

A collection of scripts for transforming ONB music score metadata into a semantically enriched knowledge graph of music scores.

## Data aggregation

Starting from the ONB's raw music score dataset (Aleph export) data aggregation involves the following steps:

+ Data normalization: extract relevant fields from raw aleph data ([example][ex_raw]) and transform to JSON ([example][ex_normalized])
+ Data enrichment ([example][ex_enriched]):
    + follow GND links in raw/normalized data and collect additional uris (e.g., DBpedia, VIAF)
    + find related Europeana items by (i) searching via the Europeana search API and (ii) filtering those that share at least one URI with the raw/normalized data
+ Statistics computation: ([example][summary_enriched])
    + id: aleph document id
    + links_artwork: number of artwork links
    + persons: number of persons mentioned in metadata record
    + links_person_gnd: number of persons linked to GND
    + links_person_dbpedia: number of persons linked to DBPedia
    + links_person_viaf: number of persons linked to VIAF
    + related_europeana_items: number of persons possibly related to Europeana

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


[ex_raw]: ./data/raw/AL00119186.xml
[ex_normalized]: ./data/normalized/AL00119186.json
[ex_enriched]: ./data/enriched/AL00119186.json

[summary_normalized]: ./summary_normalized.csv
[summary_enriched]: ./summary_enriched.csv
