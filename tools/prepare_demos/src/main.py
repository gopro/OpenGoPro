# main.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar  8 23:33:16 UTC 2023

from __future__ import annotations

import sys
import json
import argparse
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Any, ClassVar

from jsonschema import validate


@dataclass
class Demo:
    name: str
    description: str
    location: Path
    language: str

    FRONT_MATTER_TEMPLATE: ClassVar[
        str
    ] = """---
github: https://github.com/gopro/OpenGoPro/tree/main/demos/{dir}
permalink: /demos/{dir}
snippet: {snippet}
---

"""

    @classmethod
    def from_json(cls, language: str, json_str: dict[str, str]) -> Demo:
        return Demo(
            name=json_str["name"],
            description=json_str["description"],
            location=Path(json_str["location"]),
            language=language,
        )

    def lang_emoji(self, language: str) -> str:
        return "✔️" if language in self.language else  "❌"

    def create_front_matter(self) -> str:
        return self.FRONT_MATTER_TEMPLATE.format(dir=self.location, snippet=self.description)

    def as_table_entry(self) -> str:
        return f"|{self.location}|{self.description}|"


def get_demo_meta(meta: dict[str, Any], location: Path) -> Demo:
    # Get demo metadata based on location
    for language, demos in meta.items():
        for demo in demos:
            if Path(demo["location"]).parts[-2:] == location.parent.parts[-2:]:
                return Demo.from_json(language, demo)
    else:
        raise RuntimeError(f"No meta in demos.json found for {location}")


def main(args: argparse.Namespace):
    args.output.mkdir(exist_ok=True)
    shutil.rmtree(args.output)
    args.output.mkdir(exist_ok=True)

    demos: list[Demo] = []

    demos_meta: dict[str, Any]
    with open(args.input / "demos.json") as fp:
        demos_meta = json.load(fp)

    schema: dict[str, Any]
    with open(args.input / "schema.json") as fp:
        schema = json.load(fp)

    validate(demos_meta, schema)

    demos_meta = demos_meta["demos"]

    for readme in args.input.glob("**/README.md"):
        print(f"Processing {readme}")
        # Skip tutorials and top level readme
        if "tutorial" in str(readme) or readme.parts[-2] == "demos":
            continue
        demo = get_demo_meta(demos_meta, readme)

        target = args.output / demo.language / f"{demo.location.name}.md"
        target.parent.mkdir(exist_ok=True)

        # Append front matter and write to site folder
        with open(readme) as read_fp, open(target, "a") as write_fp:
            write_fp.write(demo.create_front_matter())
            write_fp.write(read_fp.read())

        demos.append(demo)

    # Create demos README.md table
    demos_readme: str
    with open(args.input / "README.md") as fp:
        demos_readme = fp.read()





def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=""" This script will perform the following:
1. Copy over demo documentation from the top-level demos folder into the docs directory for building the site
2. Add front matter to the demo documentation based on its relative path into the demos directory
3. Extract a snippet describing the demo from the README.md at the top level of the demos folder
"""
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Demo directory to search for README files. Defaults to /home/demos in Jekyll Docker container",
        default=Path("/") / "home" / "demos",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Where to write modified README's for Jekyll consumption. Defaults to /site/_demos in Jekyll Docker container",
        default=Path("/") / "site" / "_demos",
    )

    return parser.parse_args()


def entrypoint():
    try:
        main(parse_arguments())
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    entrypoint()
