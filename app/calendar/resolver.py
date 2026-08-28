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


def seventh_sunday_of_easter(year: int) -> date:
    """The Sunday between Ascension and Pentecost - a genuine, distinct gap
    in breviarium-core's own data (every other day of Easter Time has an
    entry; this one alone doesn't), so it needs its own bespoke content
    (see render_day.py's EASTER_7_SUNDAY_* constants, sourced from
    Universalis' official Latin text) rather than the usual breviarium-core
    lookup the rest of Easter Time uses."""
    return pentecost(year) - timedelta(days=7)


def christ_the_king(year: int) -> date:
    """The Solemnity of Our Lord Jesus Christ, King of the Universe - always
    the very last Sunday of Ordinary Time (the same Sunday
    last_ot_sunday_before_advent already computes for the psalter-week-
    numbering rule), closing the liturgical year. Named separately here
    because, unlike that helper, this one exists to be checked against for
    its own sake: found completely missing from the sanctorale/special-case
    system during the 2026-2029 cross-check against content/calendar/'s
    synced cache - every other year-defining Sunday (Trinity, Christ the
    King's opposite bookend) already had this kind of explicit check, this
    one didn't."""
    return last_ot_sunday_before_advent(year)


def christmas(year: int) -> date:
    return date(year, 12, 25)


@dataclass
class AdventTag:
    date: date
    breviarium_id: str   # e.g. 'advent_1_monday' or 'advent_december_17'
    week_number: int      # 1-4, or None for the December 17-24 'greater ferias'
    weekday: str          # 'Monday'..'Sunday'


def resolve_advent(d: date):
    """Return an AdventTag for d, or None if d isn't within Advent that year.
    Advent runs from the First Sunday of Advent through December 24th
    (inclusive). December 17-24 are the 'greater ferias' (O Antiphon days)
    and are indexed by calendar date rather than week+weekday - but only on
    a weekday: a Sunday keeps its own Sunday character throughout Advent
    (including Advent 4, which always falls within Dec 18-24) and is never
    given O-Antiphon-day treatment even when its date falls in that range."""
    year = d.year
    advent1 = first_sunday_of_advent(year)
    xmas = christmas(year)
    if not (advent1 <= d < xmas):
        return None

    weekday_name = d.strftime("%A")
    is_sunday = d.weekday() == 6

    if not is_sunday and date(year, 12, 17) <= d <= date(year, 12, 24):
        return AdventTag(date=d, breviarium_id=f"advent_december_{d.day}",
                          week_number=None, weekday=weekday_name)

    week_number = ((d - advent1).days // 7) + 1
    suffix = "sunday" if is_sunday else weekday_name.lower()
    return AdventTag(date=d, breviarium_id=f"advent_{week_number}_{suffix}",
                      week_number=week_number, weekday=weekday_name)


def first_sunday_of_lent(year: int) -> date:
    return ash_wednesday(year) + timedelta(days=4)  # Ash Wednesday is always a Wednesday


def palm_sunday(year: int) -> date:
    return easter_sunday(year) - timedelta(days=7)


def holy_thursday(year: int) -> date:
    """The Sacred Triduum begins with the Evening Mass of the Lord's Supper
    this same evening, replacing the usual Vespers - so this date is the
    upper bound of ferial-Lent scope, not itself included."""
    return easter_sunday(year) - timedelta(days=3)


@dataclass
class LentTag:
    date: date
    breviarium_id: str
    week_number: int      # 1-5, or None for the pre-Lent-1 days, Palm Sunday, or Holy Week
    weekday: str           # 'Monday'..'Sunday'
    is_holy_week: bool = False


_AFTER_ASH_WEDNESDAY_IDS = {
    2: "ash_wednesday", 3: "thursday_after_ash_wednesday",
    4: "friday_after_ash_wednesday", 5: "saturday_after_ash_wednesday",
}
_HOLY_WEEK_IDS = {0: "holy_monday", 1: "holy_tuesday", 2: "holy_wednesday"}


def resolve_lent(d: date):
    """Return a LentTag for d, or None if d isn't within ferial-Lent scope
    that year. Lent proper runs Ash Wednesday through the day before Holy
    Thursday (exclusive) - Holy Thursday evening through the Easter Vigil is
    the Sacred Triduum, a separate liturgical unit not handled here (see
    holy_thursday's docstring). Three sub-ranges, each with its own
    breviarium-core id scheme: Ash Wednesday through the following Saturday
    (dated ids), the five numbered Lent weeks (week+weekday ids, Palm Sunday
    excluded), and Holy Week Monday-Wednesday (dated ids again - Palm Sunday
    itself is a single named id, not part of a week)."""
    year = d.year
    aw = ash_wednesday(year)
    lent1 = first_sunday_of_lent(year)
    palm = palm_sunday(year)
    thu = holy_thursday(year)
    if not (aw <= d < thu):
        return None

    weekday_name = d.strftime("%A")

    if aw <= d < lent1:
        bid = _AFTER_ASH_WEDNESDAY_IDS.get(d.weekday())
        if bid is None:
            return None
        return LentTag(date=d, breviarium_id=bid, week_number=None, weekday=weekday_name)

    if d == palm:
        return LentTag(date=d, breviarium_id="palm_sunday_of_the_passion_of_the_lord",
                        week_number=None, weekday=weekday_name)

    if palm < d < thu:
        bid = _HOLY_WEEK_IDS.get(d.weekday())
        if bid is None:
            return None
        return LentTag(date=d, breviarium_id=bid, week_number=None, weekday=weekday_name,
                        is_holy_week=True)

    week_number = ((d - lent1).days // 7) + 1
    suffix = "sunday" if d.weekday() == 6 else weekday_name.lower()
    return LentTag(date=d, breviarium_id=f"lent_{week_number}_{suffix}",
                    week_number=week_number, weekday=weekday_name)


@dataclass
class TriduumTag:
    date: date
    breviarium_id: str
    weekday: str           # 'Thursday' | 'Friday' | 'Saturday'
    has_vespers: bool


def resolve_triduum(d: date):
    """Return a TriduumTag for d, or None if d isn't Holy Thursday, Good
    Friday, or Holy Saturday that year - the Sacred Triduum, liturgically its
    own unit distinct from both Lent (which ends the moment Holy Thursday
    begins, see holy_thursday's docstring) and Easter Time (which begins at
    Easter Sunday, not before). Per GILH SS208-211: Lauds is celebrated as
    usual on all three days. Vespers exists for Holy Thursday and Good Friday
    - skipped only by those attending that evening's liturgical celebration
    (the Mass of the Lord's Supper / the Celebration of the Lord's Passion),
    so it's still rendered here as real content for everyone else, the same
    policy this project already applies to a Sunday's anticipated Saturday-
    evening Vespers. Holy Saturday is different: SS208-209 name only Thursday
    and Friday as having a Vespers that can be skipped - Saturday's doesn't
    exist to skip, because the Easter Vigil replaces it structurally, not
    just pastorally (has_vespers=False signals the caller to say so rather
    than render nothing)."""
    year = d.year
    thu = holy_thursday(year)
    fri = thu + timedelta(days=1)
    sat = thu + timedelta(days=2)
    if d == thu:
        return TriduumTag(date=d, breviarium_id="holy_thursday", weekday="Thursday", has_vespers=True)
    if d == fri:
        return TriduumTag(date=d, breviarium_id="friday_of_the_passion_of_the_lord", weekday="Friday", has_vespers=True)
    if d == sat:
        return TriduumTag(date=d, breviarium_id="holy_saturday", weekday="Saturday", has_vespers=False)
    return None


def transferred_solemnity_date(year: int, month: int, day: int):
    """Where a fixed-date Solemnity (month/day) is impeded that year - by a
    Privileged Sunday (of Advent, Lent, or Easter) or by Holy Week/the
    Triduum/the Easter Octave, all of which outrank a General Solemnity per
    UNLY Table #59 (tiers 1-2 vs tier 3) - returns the date it's actually
    celebrated on instead; returns None in the ordinary case (not impeded
    that year). Two shapes, both confirmed against real cases in this
    project's 2026-2029 window: landing on a plain Sunday of Advent or Lent
    moves it to the very next day, Monday (St Joseph, 2028: Mar 19 is the
    3rd Sunday of Lent, so he's kept on Mar 20 instead); landing anywhere
    from Palm Sunday through Divine Mercy Sunday has no free day until the
    Monday right after that whole block (the Annunciation, both 2027 - Mar 25
    is Holy Thursday itself - and 2029 - Mar 25 is Palm Sunday - land here,
    both correctly resolving to the Monday after Divine Mercy Sunday, which
    is the commonly-cited transfer target for this specific Solemnity)."""
    d = date(year, month, day)
    palm = palm_sunday(year)
    dms = easter_sunday(year) + timedelta(days=7)  # Divine Mercy Sunday
    if palm <= d <= dms:
        return dms + timedelta(days=1)
    if d.weekday() == 6:
        aw = ash_wednesday(year)
        advent1 = first_sunday_of_advent(year)
        christmas = date(year, 12, 25)
        if (aw <= d < palm) or (advent1 <= d < christmas):
            return d + timedelta(days=1)
    return None


_EASTER_OCTAVE_WEEKDAY_IDS = {
    6: "easter_sunday", 0: "easter_monday", 1: "easter_tuesday", 2: "easter_wednesday",
    3: "easter_thursday", 4: "easter_friday", 5: "easter_saturday",
}


@dataclass
class EasterTag:
    date: date
    breviarium_id: str
    week_number: int      # 2-7, or None for the Octave or a named Solemnity
    weekday: str           # 'Monday'..'Sunday'


def resolve_easter(d: date):
    """Return an EasterTag for d, or None if d isn't within Easter Time that
    year. The season runs Easter Sunday through Pentecost Sunday inclusive
    (Trinity Sunday, the following Sunday, is its own separate Solemnity,
    not part of Easter Time itself, so it's out of scope here). Three
    sub-ranges: the Octave (Easter Sunday through the following Saturday,
    each day keeping the full solemnity of Easter itself - dated-by-weekday
    ids), Ascension/Pentecost (named ids - this project follows the General
    Calendar's traditional Thursday Ascension, not the Sunday-transferred
    convention some episcopal conferences use, matching content/calendar/'s
    already-synced cache), and the six numbered Easter weeks in between
    (week+weekday ids, Divine Mercy Sunday named separately rather than as
    'easter_time_2_sunday')."""
    year = d.year
    easter = easter_sunday(year)
    pent = pentecost(year)
    if not (easter <= d <= pent):
        return None

    weekday_name = d.strftime("%A")

    if d < easter + timedelta(days=7):
        bid = _EASTER_OCTAVE_WEEKDAY_IDS[d.weekday()]
        return EasterTag(date=d, breviarium_id=bid, week_number=None, weekday=weekday_name)

    if d == easter + timedelta(days=7):
        return EasterTag(date=d, breviarium_id="divine_mercy_sunday", week_number=None, weekday=weekday_name)

    if d == easter + timedelta(days=39):
        return EasterTag(date=d, breviarium_id="ascension_of_the_lord", week_number=None, weekday=weekday_name)

    if d == pent:
        return EasterTag(date=d, breviarium_id="pentecost_sunday", week_number=None, weekday=weekday_name)

    week_number = ((d - easter).days // 7) + 1
    suffix = "sunday" if d.weekday() == 6 else weekday_name.lower()
    return EasterTag(date=d, breviarium_id=f"easter_time_{week_number}_{suffix}",
                      week_number=week_number, weekday=weekday_name)


def holy_family(year: int) -> date:
    """The Sunday within the Octave of Christmas (Dec 26-31); if Christmas
    Day itself is a Sunday, Holy Family is celebrated on December 30
    instead (there being no other Sunday in the Octave that year)."""
    if christmas(year).weekday() == 6:
        return date(year, 12, 30)
    return _sunday_on_or_after(date(year, 12, 26))


@dataclass
class ChristmasTag:
    date: date
    breviarium_id: str
    weekday: str


def resolve_christmas(d: date):
    """Return a ChristmasTag for d, or None if d isn't within the ferial-
    Christmas-season gaps this handles. Christmas Day, Mary Mother of God
    (Jan 1), and Epiphany (Jan 6) are already fixed-date Solemnities in
    content/sanctorale/ and are NOT re-handled here - this only covers what
    that fixed-date system structurally can't: Holy Family (a movable Sunday
    within a fixed range) and the plain ferial days of the Octave, the
    stretch between the Octave and Epiphany, and the stretch between
    Epiphany and the Baptism of the Lord (also already in sanctorale, as
    the upper bound here)."""
    year = d.year
    xmas = christmas(year)
    epi = epiphany(year)
    baptism = baptism_of_the_lord(year)

    if xmas < d <= date(year, 12, 31):
        weekday_name = d.strftime("%A")
        if d == holy_family(year):
            return ChristmasTag(date=d, breviarium_id="holy_family_of_jesus_mary_and_joseph", weekday=weekday_name)
        day_number = (d - xmas).days + 1  # Christmas Day itself is day 1
        return ChristmasTag(date=d, breviarium_id=f"christmas_octave_day_{day_number}", weekday=weekday_name)

    if date(year, 1, 2) <= d < epi:
        weekday_name = d.strftime("%A")
        if d.weekday() == 6:
            return ChristmasTag(date=d, breviarium_id="second_sunday_after_christmas", weekday=weekday_name)
        return ChristmasTag(date=d, breviarium_id=f"christmas_time_january_{d.day}", weekday=weekday_name)

    if epi < d < baptism:
        weekday_name = d.strftime("%A")
        return ChristmasTag(date=d, breviarium_id=f"{weekday_name.lower()}_after_epiphany", weekday=weekday_name)

    return None


def most_holy_trinity(year: int) -> date:
    """The Sunday after Pentecost - its own separate Solemnity, not part of
    Easter Time (which ends at Pentecost), but it must still be checked for
    explicitly: its date otherwise falls inside Ordinary Time Part 2's
    range (which starts the day after Pentecost) and would be wrongly
    claimed as that part's first Sunday without this override."""
    return pentecost(year) + timedelta(days=7)


def mary_mother_of_the_church(year: int) -> date:
    """Monday after Pentecost - added to the General Calendar in 2018."""
    return pentecost(year) + timedelta(days=1)


def corpus_christi(year: int) -> date:
    """Thursday after Trinity Sunday. Some episcopal conferences transfer
    this to the following Sunday; this project follows the General
    Calendar's Thursday, matching the already-synced content/calendar/
    cache and the same convention already used for Ascension."""
    return most_holy_trinity(year) + timedelta(days=4)


def sacred_heart_of_jesus(year: int) -> date:
    """Friday in the third week after Pentecost (19 days after Pentecost
    Sunday, always a Friday)."""
    return pentecost(year) + timedelta(days=19)


def immaculate_heart_of_mary(year: int) -> date:
    """The Saturday immediately after the Solemnity of the Sacred Heart."""
    return sacred_heart_of_jesus(year) + timedelta(days=1)


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
    # A date in early January could in principle belong to the previous
    # year's OT Part 2, but that case doesn't occur for the General Calendar
    # (Part 2 always ends before Advent 1, which is always in the same civil
    # year as Christmas), so no year-rollover handling is needed here.

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


@dataclass
class SundayOrdinaryTimeTag:
    date: date
    ot_week_number: int      # 1-34, the Sunday's own week number
    psalter_week: int        # 1-4, derived from ot_week_number


def resolve_ordinary_time_sunday(d: date):
    """Return a SundayOrdinaryTimeTag for d, or None if d isn't a Sunday in
    Ordinary Time. Same week-numbering rule as the ferial resolver, just
    evaluated with d itself as the governing Sunday (no need to search
    backward for one)."""
    if d.weekday() != 6:
        return None

    year = d.year
    part1_start, part1_end = start_of_ordinary_time_part1(year), end_of_ordinary_time_part1(year)
    part2_start, part2_end = start_of_ordinary_time_part2(year), end_of_ordinary_time_part2(year)

    if part1_start <= d <= part1_end:
        week_number = ((d - baptism_of_the_lord(year)).days // 7) + 1
    elif part2_start <= d <= part2_end:
        anchor = last_ot_sunday_before_advent(year)
        week_number = 34 - ((anchor - d).days // 7)
    else:
        return None  # Advent, Christmas, Lent, or Easter season - not handled yet

    psalter_week = ((week_number - 1) % 4) + 1
    return SundayOrdinaryTimeTag(date=d, ot_week_number=week_number, psalter_week=psalter_week)
