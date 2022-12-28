import csv
import requests
from dagster import asset


@asset
def cereals():
    response = requests.get("https://docs.dagster.io/assets/cereal.csv")
    lines = response.text.split("\n")
    cereal_rows = [row for row in csv.DictReader(lines)]

    return cereal_rows


# NOTE: To take advantage of Dagster's incremental re-execution functionality (e.g. retry from failure),
# you'll need to set up an IO manager that can move the data across runs.
# For more details, visit https://docs.dagster.io/concepts/io-management/io-managers#applying-io-managers-to-assets
