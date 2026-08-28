"""Calendar resolver: date -> liturgical tag, for the General (Universal) Roman Calendar.

Phase 1 scope: ferial (non-Sunday, non-feast) Ordinary Time only. Sundays, the
Proper of Seasons/Saints, and feast/memorial precedence are deferred to later
phases and are NOT handled here yet - dates outside ferial Ordinary Time
resolve to an "out_of_scope" tag rather than a wrong answer.

The Ordinary Time week-numbering rule (the trickiest part of this module) is
sourced from the General Instruction of the Liturgy of the Hours / Universal
Norms on the Liturgical Year: the last Sunday before Advent 1 is always week
34, and Ordinary Time Part 2 (after Pentecost) is numbered by counting
backward from that anchor - this single rule automatically reproduces both
the "34 total weeks" and "33 total weeks, one number skipped" cases without
a separate branch, since which case applies is just how many Sundays happen
to fit between Pentecost and Advent that year.

This module has NOT yet been cross-validated against a published Ordo for
multiple years - see docs/calendar_resolver_notes.md before trusting output
for anything beyond Phase 1 development.
"""
from dataclasses import dataclass
from datetime import date, timedelta


def easter_sunday(year: int) -> date:
    """Gregorian Easter Sunday (Meeus/Jones/Butcher algorithm)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def ash_wednesday(year: int) -> date:
    return easter_sunday(year) - timedelta(days=46)


def pentecost(year: int) -> date:
    return easter_sunday(year) + timedelta(days=49)


def epiphany(year: int) -> date:
    """Universal (General Roman) Calendar: fixed January 6, not transferred to Sunday."""
    return date(year, 1, 6)


def _sunday_on_or_before(d: date) -> date:
    # date.weekday(): Monday=0 ... Sunday=6
    return d - timedelta(days=(d.weekday() + 1) % 7)


def _sunday_on_or_after(d: date) -> date:
    offset = (6 - d.weekday()) % 7
    return d + timedelta(days=offset)


def baptism_of_the_lord(year: int) -> date:
    epi = epiphany(year)
    if epi.weekday() == 6:  # Epiphany itself falls on a Sunday
        return epi + timedelta(days=1)  # moves to the following Monday
    return _sunday_on_or_after(epi)


def first_sunday_of_advent(year: int) -> date:
    """The Sunday closest to November 30th (equivalently, 4th Sunday before Christmas)."""
    christmas = date(year, 12, 25)
    return _sunday_on_or_before(christmas) - timedelta(weeks=3)


def start_of_ordinary_time_part1(year: int) -> date:
    return baptism_of_the_lord(year) + timedelta(days=1)


def end_of_ordinary_time_part1(year: int) -> date:
    return ash_wednesday(year) - timedelta(days=1)


def start_of_ordinary_time_part2(year: int) -> date:
    return pentecost(year) + timedelta(days=1)


def end_of_ordinary_time_part2(year: int) -> date:
    return first_sunday_of_advent(year) - timedelta(days=1)


def last_ot_sunday_before_advent(year: int) -> date:
    return first_sunday_of_advent(year) - timedelta(weeks=1)


@dataclass
class FerialOrdinaryTimeTag:
    date: date
    ot_week_number: int      # 1-34, per the official Ordinary Time count
    psalter_week: int        # 1-4, derived from ot_week_number
    weekday: str             # "Monday".."Saturday" (Sunday out of Phase 1 scope)


def resolve_ferial_ordinary_time(d: date):
    """Return a FerialOrdinaryTimeTag for d, or None if d is out of Phase 1 scope
    (a Sunday, or outside the two Ordinary Time ranges for its year)."""
    if d.weekday() == 6:  # Sunday - deferred to a later phase
        return None

    year = d.year
    # A date in early January может belong to the previous year's OT Part 2
    # only in edge cases that don't occur for the General Calendar (Part 2
    # always ends before Advent 1, which is always in the same civil year as
    # Christmas), so no year-rollover handling is needed here.

    part1_start, part1_end = start_of_ordinary_time_part1(year), end_of_ordinary_time_part1(year)
    part2_start, part2_end = start_of_ordinary_time_part2(year), end_of_ordinary_time_part2(year)

    if part1_start <= d <= part1_end:
        governing_sunday = _sunday_on_or_before(d)
        week_number = ((governing_sunday - baptism_of_the_lord(year)).days // 7) + 1
    elif part2_start <= d <= part2_end:
        governing_sunday = _sunday_on_or_before(d)
        anchor = last_ot_sunday_before_advent(year)
        week_number = 34 - ((anchor - governing_sunday).days // 7)
    else:
        return None  # Advent, Christmas, Lent, or Easter season - not handled yet

    psalter_week = ((week_number - 1) % 4) + 1
    weekday_name = d.strftime("%A")
    return FerialOrdinaryTimeTag(date=d, ot_week_number=week_number,
                                  psalter_week=psalter_week, weekday=weekday_name)
