"""
A collection of commonly use data manipulation procedures.

"""

import json
import os


def progress(progress=0):
    progress = round(progress * 100)
    print("\n*** Progress: {0}% ***".format(progress))


# I/O handling

def read_records(inputfiles):
    for filename in inputfiles:
        with open(filename, 'r') as in_file:
            data = in_file.read()
            yield (filename, data)


def ensure_directory(outputdir):
    """Make sure that output directory exists"""
    if not os.path.exists(outputdir):
        print("Creating directory", outputdir)
        os.makedirs(outputdir)


def write_json_file(outputdir, filename, data):
    ensure_directory(outputdir)
    with open(outputdir + "/" + filename, "w") as out_file:
            json.dump(data, out_file, sort_keys=True, indent=4,
                      ensure_ascii=False)
