# Calendar resolver — validation status

## Verified
- Easter Sunday (Computus): matches known published dates for 2023-2028 exactly.
- Ash Wednesday, Pentecost: fixed day-offsets from Easter, no independent risk beyond Easter itself.
- Ordinary Time week numbering rule: sourced directly from a description of the
  General Instruction of the Liturgy of the Hours / Universal Norms on the
  Liturgical Year (see chat history for the citation) - the last Sunday
  before Advent 1 is always week 34, Part 2 (after Pentecost) is numbered by
  counting backward from that anchor. This single rule reproduces both the
  "34 total weeks" and "33 total weeks, one number skipped" cases without a
  separate branch.

## Independently validated (2026-07-30)
Cross-checked every day of calendar year 2026 against the Liturgical Calendar
API (litcal.johnromanodorazio.com, Apache-2.0, led by Fr. John R. D'Orazio
and the Open Source Catholic community) via its `psalter_week` and
`event_key` (which embeds the Ordinary Time week number) fields. Result:
**126/126 ferial Ordinary Time weekdays matched exactly** on both psalter
week and Ordinary Time week number - zero mismatches. This validates the
Computus implementation and the "count backward from week 34" Ordinary Time
logic against a real, independently-maintained authority, not just internal
self-consistency.

Validation script: see chat history / docs - fetches
`https://litcal.johnromanodorazio.com/api/dev/calendar/{year}` and diffs
against `resolve_ferial_ordinary_time` for every day of the year.

## Not yet covered
- The Baptism of the Lord date rule itself wasn't separately isolated in
  this validation (it's implicitly correct since it feeds the week-1 anchor
  that everything else matched against), but hasn't been checked in years
  where Jan 6 falls on a Saturday or Sunday specifically.
- Sundays, the Proper of Seasons, and feasts/memorials/solemnities are not
  implemented at all yet - `resolve_ferial_ordinary_time` returns `None` for
  any date outside ferial Ordinary Time (Monday-Saturday, Part 1 or Part 2).
  The same Liturgical Calendar API also carries feast/memorial/season data
  for every day, so it's a good candidate source for building out that next
  phase rather than re-deriving the precedence rules from scratch.
