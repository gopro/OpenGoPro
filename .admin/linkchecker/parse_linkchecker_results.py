# parse_linkchecker_results.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri May 19 19:39:24 UTC 2023

from __future__ import annotations
import sys
import csv
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Error:
    url_relative: str
    parentname: str
    base: str
    result: str
    warningstring: str
    infostring: str
    valid: bool
    url: str
    line: int
    column: int
    name: str
    dltime: int
    size: int
    checktime: float
    cached: int
    level: int
    modified: str

    ALLOWABLE_ERRORS: ClassVar[list[str]] = [
        str(error)
        for error in [
            200,
            403,
            500,
            501,
            502,
            503,
            504,
            505,
            506,
            507,
            508,
            509,
            510,
        ]
    ]

    def __post_init__(self) -> None:
        self.result = self.result.split(" ")[0].strip(":")

    @classmethod
    def from_csv(cls, csv_entry: list[str]) -> Error:
        return Error(
            *[
                *csv_entry[:6],  # url, parentname, base, result, warningstring, infostring
                True if csv_entry[6] == "True" else False,  # valid
                csv_entry[7],  # url_relative
                int(csv_entry[8]),  # line
                int(csv_entry[9]),  # column
                csv_entry[10],  # name
                int(csv_entry[11]),  # dltime
                int(csv_entry[12]),  # size
                float(csv_entry[13]),  # checktime
                int(csv_entry[14]),  # int
                int(csv_entry[15]),  # int
                csv_entry[16],  # modified
            ]
        )

    def __str__(self) -> str:
        return json.dumps({"url": self.url, "parent": self.parentname, "result": self.result}, indent=4)

    @property
    def is_our_error(self) -> bool:
        return self.result not in Error.ALLOWABLE_ERRORS


def main(args: argparse.Namespace) -> int:
    errors: list[Error] = []
    # Accumulate errors from csv file
    with open(args.input, "r") as fp:
        csv_reader = csv.reader(fp, delimiter=";")
        for entry in csv_reader:
            # Skip comments and header line
            if len(entry) > 1 and entry[0] != "urlname":
                errors.append(Error.from_csv(entry))

    # Filter out our errors
    our_errors = [error for error in errors if error.is_our_error]

    # Write output
    print(f"Found {len(our_errors)} errors that are our fault")
    if our_errors:
        print("😟 See our errors here:")
        print("\n".join([str(error) for error in our_errors]))
        return 1
    else:
        print("😃 SUCCESS!!")
        return 0


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse Linkchecker output to search for errors that are our fault.",
    )
    parser.add_argument(
        "input",
        type=Path,
        help=f"Linkchecker results file",
    )

    return parser.parse_args()


def entrypoint() -> int:
    return main(parse_arguments())


if __name__ == "__main__":
    sys.exit(entrypoint())