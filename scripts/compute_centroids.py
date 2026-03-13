#!/usr/bin/env python3
"""Compute SVG path centroids and rewrite quiz data files with label coordinates."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from svgpathtools import parse_path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
DATA = ROOT / "src" / "geoquiz" / "data"

# Map data file -> SVG template (must match Quiz.map_template values)
QUIZ_MAPS = {
    "europe_countries.py": "maps/europe.svg",
    "africa_countries.py": "maps/africa.svg",
    "asia_countries.py": "maps/asia.svg",
    "north_america_countries.py": "maps/north_america.svg",
    "south_america_countries.py": "maps/south_america.svg",
    "oceania_countries.py": "maps/oceania.svg",
    "us_states.py": "maps/us_states.svg",
}


def find_path_strings(root: ET.Element, entry_id: str) -> list[str]:
    """Find SVG path d-strings for an entry ID (handles <path> and <g> elements)."""
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    for el in root.iter():
        eid = el.get("id")
        if eid and eid.lower() == entry_id.lower():
            tag = el.tag.replace(ns, "")
            if tag == "g":
                return [
                    p.get("d")
                    for p in el.iter()
                    if p.tag.replace(ns, "") == "path" and p.get("d")
                ]
            elif tag == "path":
                d = el.get("d")
                return [d] if d else []
    return []


def compute_centroid(path_strings: list[str], samples: int = 40) -> tuple[float, float] | None:
    """Compute length-weighted centroid by sampling points along SVG paths."""
    cx, cy, total_weight = 0.0, 0.0, 0.0
    for d in path_strings:
        try:
            path = parse_path(d)
            length = path.length()
            if length == 0:
                continue
            sx, sy = 0.0, 0.0
            for i in range(samples):
                pt = path.point(i / samples)
                sx += pt.real
                sy += pt.imag
            cx += (sx / samples) * length
            cy += (sy / samples) * length
            total_weight += length
        except Exception:
            continue
    if total_weight == 0:
        return None
    return (round(cx / total_weight, 1), round(cy / total_weight, 1))


def update_data_file(data_file: Path, centroids: dict[str, tuple[float, float]]) -> None:
    """Rewrite a data file, adding label_x/label_y to each QuizEntry."""
    content = data_file.read_text()

    for entry_id, (lx, ly) in centroids.items():
        # Match QuizEntry("id", ...) and inject/replace label coords
        pattern = rf'(QuizEntry\("{re.escape(entry_id)}"[^)]*?)(,\s*label_[xy]=[0-9.]+)*(,\s*label_[xy]=[0-9.]+)*\)'
        match = re.search(pattern, content)
        if match:
            # Strip any existing label_x/label_y, then append new ones
            core = match.group(1)
            core = re.sub(r",\s*label_[xy]=[0-9.]+", "", core)
            replacement = f"{core}, label_x={lx}, label_y={ly})"
            content = content[: match.start()] + replacement + content[match.end() :]

    data_file.write_text(content)


def main() -> None:
    for data_filename, svg_rel in QUIZ_MAPS.items():
        svg_path = TEMPLATES / svg_rel
        data_path = DATA / data_filename

        if not svg_path.exists():
            print(f"SKIP {data_filename}: {svg_path} not found")
            continue

        print(f"\n{data_filename}:")
        root = ET.parse(svg_path).getroot()
        content = data_path.read_text()

        # Extract all entry IDs from the data file
        entry_ids = re.findall(r'QuizEntry\("([^"]+)"', content)
        centroids: dict[str, tuple[float, float]] = {}

        for eid in entry_ids:
            paths = find_path_strings(root, eid)
            if not paths:
                print(f"  WARN {eid}: no SVG element found")
                continue
            centroid = compute_centroid(paths)
            if not centroid:
                print(f"  WARN {eid}: centroid computation failed")
                continue
            centroids[eid] = centroid
            print(f"  {eid}: ({centroid[0]}, {centroid[1]})")

        update_data_file(data_path, centroids)
        print(f"  -> Updated {len(centroids)}/{len(entry_ids)} entries")


if __name__ == "__main__":
    main()
