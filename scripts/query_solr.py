#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

import requests


def fetch_solr_results(query_file, query_cfg, solr_uri, collection):
    """
    Fetch search results from a Solr instance based on the query parameters.

    Arguments:
    - query_file: Path to the JSON file containing Solr query parameters.
    - solr_uri: URI of the Solr instance (e.g., http://localhost:8983/solr).
    - collection: Solr collection name from which results will be fetched.

    Output:
    - Prints the JSON search results to STDOUT.
    """
    # Load the query parameters from the JSON file
    try:
        query_text = json.load(open(query_file))["query_text"]
        query_params = json.load(open(query_cfg))

    except FileNotFoundError:
        sys.exit(1)

    # Build actual query using query_config
    query_params["query"] = query_text

    # Construct the Solr request URL
    uri = f"{solr_uri}/{collection}/select"

    try:
        # Send the POST request to Solr
        response = requests.post(uri, json=query_params)
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)

    # Fetch and print the results as JSON
    results = response.json()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    # Set up argument parsing for the command-line interface
    parser = argparse.ArgumentParser(
        description="Fetch search results from Solr and output them in JSON format."
    )

    parser.add_argument(
        "--query",
        type=Path,
        required=True,
        help="Path to the JSON file containing the Solr query input text.",
    )

    parser.add_argument(
        "--query_cfg",
        type=Path,
        required=True,
        help="Path to the JSON file containing configuration parameters.",
    )

    parser.add_argument(
        "--uri",
        type=str,
        default="http://localhost:8983/solr",
        help="The URI of the Solr instance (default: http://localhost:8983/solr).",
    )

    parser.add_argument(
        "--collection",
        type=str,
        default="courses",
        help="Name of the Solr collection to query (default: 'courses').",
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    fetch_solr_results(args.query, args.query_cfg, args.uri, args.collection)
