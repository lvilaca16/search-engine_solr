import argparse
import json
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List

from tqdm import tqdm


@dataclass(frozen=True)
class Record:
    """
    Class for representing a Record (paper in the CF dataset).
    """

    abstract: str
    authors: List[str]
    major_subj: List[str]
    minor_subj: List[str]
    id: int
    #record_n: str
    source: str
    title: str

    def to_dict(self):
        return {v.name: getattr(self, v.name) for v in fields(self)}


@dataclass(frozen=True)
class Query:
    """
    Class for representing a Query (and its relevance scores).
    """

    query_n: str
    query_text: str
    qrels: List[str]

    def to_dict(self):
        return {v.name: getattr(self, v.name) for v in fields(self)}


def get_list(tree, tag: str, qrel: bool = False) -> List[str]:
    """
    Get list of sub-attributes in an .XML sub tree.

    Arguments:
        record -- .XML tree.
        tag -- First level subtree tag.

    Returns:
        List of elements within the subtree obtained from the tag.
    """
    subtree = tree.find(tag)

    # Query relevance scores
    if qrel:
        qrel_list = []

        for doc in subtree.iter("Item"):
            # Consider as relevant the highly and marginally relevant documents
            # Qrels were annotated by post-doctorates, for more information
            # read the original CF documentation (data/))
            rel_score = doc.get("score")[-2]

            if int(rel_score) > 0:
                qrel_list.append(doc.text)

        return qrel_list

    # Records
    else:
        if subtree is None:
            return ""

        return [x.text for x in subtree.iter() if x.text is not None]


def text_preproc(text: str) -> str:
    """
    Remove unwanted characters/text from string.

    Arguments:
        text -- input string

    Returns:
        Cleaned string.
    """
    return re.sub(" +", " ", text.replace("\n", " "))


def main(config_path: Path, verbose: bool) -> None:

    # Load configs
    with open(config_path.as_posix(), encoding="utf-8") as f:
        config = json.loads(f.read())

    dataset = []

    # Preprocess records
    for file in config["dataset"]["data_files"]:

        tree = ET.parse(file)
        root = tree.getroot()

        for record in tqdm(root.findall("RECORD")):

            # Abstract can contain two different tags
            if record.find("ABSTRACT") is None:
                text = record.find("EXTRACT").text
            else:
                text = record.find("ABSTRACT").text

            record = Record(
                text_preproc(text),
                get_list(record, "AUTHORS"),
                get_list(record, "MAJORSUBJ"),
                get_list(record, "MINORSUBJ"),
                int(text_preproc(record.find("RECORDNUM").text)),
                text_preproc(record.find("SOURCE").text),
                text_preproc(record.find("TITLE").text),
            )

            dataset.append(record.to_dict())

    if verbose:
        print(f"{len(dataset)} documents acquired")

    output_path = Path(config["output"]).joinpath("data.json")

    # Save records
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=4)

    # Preprocess qrels
    for file in config["dataset"]["qrels"]:

        tree = ET.parse(file)
        root = tree.getroot()

        for query in tqdm(root.findall("QUERY")):

            query = Query(
                text_preproc(query.find("QueryNumber").text),
                text_preproc(query.find("QueryText").text),
                get_list(query, "Records", qrel=True),
            )

            if verbose:
                print(f"Query {query.query_n} has {len(query.qrels)} QRELS.")

            output_path = Path(config["output"])
            os.makedirs(output_path.joinpath("qrels"), exist_ok=True)

            output_path = output_path.joinpath(f"qrels/{query.query_n}.json")

            # Save qrels
            with open(output_path, "w") as f:
                json.dump(query.to_dict(), f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config_path",
        type=str,
        required=False,
        default="config/config.json",
        help="Path to configuration file.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Activate verbose mode for detailed output.",
    )

    args = parser.parse_args()

    config = json.loads

    main(Path(args.config_path), bool(args.verbose))
