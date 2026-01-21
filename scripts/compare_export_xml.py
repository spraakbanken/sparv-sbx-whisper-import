#!/usr/bin/env python
"""Script to compare actual xml with snapshot xml in a stable way."""

import argparse
import sys
from itertools import zip_longest
from xml.etree import ElementTree as ET


def main(snapshot_path: str, actual_path: str) -> None:
    """Compare 2 xml."""
    snapshot_root = ET.parse(snapshot_path).getroot()
    actual_root = ET.parse(actual_path).getroot()

    errors = []
    _compare_elements(snapshot_root, actual_root, errors)

    if len(errors) > 0:
        print("Found the following errors", file=sys.stderr)  # noqa: T201
        for error in errors:
            print(f"  {error}", file=sys.stderr)  # noqa: T201
        sys.exit(1)


def _compare_elements(snapshot_elem: ET.Element, actual_elem: ET.Element, errors: list[str]) -> None:
    if snapshot_elem.tag == "token" or actual_elem.tag == "token":
        return
    if snapshot_elem.tag != actual_elem.tag:
        errors.append(f"Tag mismatch: {snapshot_elem.tag} != {actual_elem.tag}")
    _compare_attributes(snapshot_elem, actual_elem, errors)


def _compare_attributes(
    snapshot_elem: ET.Element,
    actual_elem: ET.Element,
    errors: list[str],
) -> None:
    snapshot_attrs = sorted(snapshot_elem.attrib.items())
    actual_attrs = sorted(actual_elem.attrib.items())

    for snapshot_attr_value, actual_attr_value in zip_longest(snapshot_attrs, actual_attrs):
        if snapshot_attr_value is None:
            errors.append(f"Actual contains extra attribute: '{actual_attr_value}'")
            continue
        if actual_attr_value is None:
            errors.append(f"Snapshot contains extra attribute: '{snapshot_attr_value}'")
            continue
        (snapshot_attr, snapshot_value) = snapshot_attr_value
        (actual_attr, actual_value) = actual_attr_value
        if snapshot_attr != actual_attr:
            errors.append(f"Attribute name mismatch: '{snapshot_attr}' != '{actual_attr}'")
            return
        if snapshot_value != actual_value:
            errors.append(f"Attribute value mismatch for {snapshot_attr}: '{snapshot_value}' != '{actual_value}'")


def _elem_to_str(elem: ET.Element) -> str:
    attrib_str = " ".join(f'{attr}="{value}"' for attr, value in elem.attrib.items())
    return f"<{elem.tag}{' ' if attrib_str else ''}{attrib_str}>{elem.text}</{elem.tag}>"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare the snapshot and actual XML files.")
    parser.add_argument("snapshot", type=str)
    parser.add_argument("actual", type=str)

    args = parser.parse_args()

    main(snapshot_path=args.snapshot, actual_path=args.actual)
