"""Sync a year of calendar data from the Liturgical Calendar API
(litcal.johnromanodorazio.com, Apache-2.0) into a local cache file.

This is a periodic sync, not a runtime dependency - run it once per year
(or whenever the calendar might have changed, e.g. a new canonization) and
commit the resulting file. The app itself never needs to call the API to
know what day it is.

Precedence rule (grade field): 3 and above (obligatory memorial, feast,
solemnity, ...) replaces the ferial day outright. 1-2 (commemoration,
optional memorial) are available alternatives to the ferial Office, not
replacements - per real liturgical law, an optional memorial gives a choice,
it doesn't force itself on the day.
"""
import json
import urllib.request
from collections import defaultdict
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "calendar"
OUT_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://litcal.johnromanodorazio.com/api/dev/calendar/{year}"
REPLACES_FERIAL_GRADE = 3


def fetch_year(year: int) -> list:
    req = urllib.request.Request(API_URL.format(year=year), headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))["litcal"]


def build_day_index(events: list) -> dict:
    by_date = defaultdict(list)
    for e in events:
        by_date[e["date"][:10]].append(e)

    days = {}
    for d, day_events in by_date.items():
        day_events.sort(key=lambda e: -e["grade"])
        primary_candidates = [e for e in day_events if e["grade"] >= REPLACES_FERIAL_GRADE]
        ferial = next((e for e in day_events if e["grade"] == 0), None)
        primary = primary_candidates[0] if primary_candidates else ferial
        if primary is None:
            primary = day_events[0]
        alternatives = [e for e in day_events if e is not primary and 1 <= e["grade"] <= 2]

        days[d] = {
            "primary": {
                "event_key": primary["event_key"], "name": primary["name"],
                "grade": primary["grade"], "grade_lcl": primary["grade_lcl"],
                "season": primary["liturgical_season"], "psalter_week": primary["psalter_week"],
                "color": primary["color"],
            },
            "optional_alternatives": [
                {"event_key": a["event_key"], "name": a["name"], "grade": a["grade"], "grade_lcl": a["grade_lcl"]}
                for a in alternatives
            ],
        }
    return days


def main(year: int):
    # The API's "year" is a liturgical year starting at Advent (late November
    # of the previous civil year), so a civil year's December falls into the
    # NEXT liturgical year's fetch. Pull both and merge to get full Jan-Dec
    # civil-year coverage.
    days = {}
    for y in (year, year + 1):
        print(f"Fetching litcal year {y} from {API_URL.format(year=y)} ...")
        events = fetch_year(y)
        days.update(build_day_index(events))

    civil_year_days = {d: v for d, v in days.items() if d.startswith(str(year))}

    out_path = OUT_DIR / f"{year}.json"
    payload = {
        "_source": ("Synced from the Liturgical Calendar API (litcal.johnromanodorazio.com), "
                    "Apache-2.0, General Roman Calendar. Merged from two API 'litcal years' "
                    "(the API's year runs Advent-to-Advent, not Jan-Dec) to cover this full civil "
                    "year. This is a periodic local cache, not a live dependency - the app reads "
                    "this file, it does not call the API at runtime. Re-sync periodically (e.g. "
                    "yearly, or after a canonization/calendar change)."),
        "year": year,
        "days": civil_year_days,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(civil_year_days)} days -> {out_path}")


if __name__ == "__main__":
    import sys
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    main(year)
