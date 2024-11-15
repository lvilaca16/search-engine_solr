#!/usr/bin/env python3

import json
from argparse import ArgumentParser
from pathlib import Path


def qrels_to_trec(qrels: list) -> None:
    """
    Converts qrels (query relevance judgments) to TREC evaluation format.

    Arguments:
    - qrels: A list of qrel lines (document IDs) from standard input.
    """
    for line in qrels:
        doc_id = line.strip()
        print(f"0 0 {doc_id} 1")


if __name__ == "__main__":
    """
    Read qrels from file and output them in TREC format.
    """
    parser = ArgumentParser(description="Convert QRELs to TREC format")

    parser.add_argument(
        "--qrels",
        type=Path,
        default="docker/data/qrels/00001.json",
        help="Path to QREL data.",
    )

    args = parser.parse_args()

    qrels = json.load(open(args.qrels))["qrels"]

    qrels_to_trec(qrels)
