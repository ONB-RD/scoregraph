"""
A collection of commonly use data manipulation procedures.

"""

import json
import os
import sys


def progress(progress=0):
    progress = int(progress * 100)
    sys.stdout.write("\rProgress: {0}%".format(progress))
    sys.stdout.flush()


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
