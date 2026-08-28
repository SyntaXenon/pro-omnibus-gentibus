"""Localization helpers for UI chrome (structural labels, weekday names,
ordinal week phrasing) - NOT liturgical content, just interface text, so
these are original short phrases safe for me to write directly rather than
sourced/flagged content.
"""

WEEKDAY_NAMES = {
    "en": {"Sunday": "Sunday", "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
           "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday"},
    "es": {"Sunday": "Domingo", "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
           "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado"},
    # Ecclesiastical Latin weekday naming convention (Feria II = Monday, etc.),
    # not the classical/astrological names - matches how the antiphons source text itself is organized.
    "la": {"Sunday": "Dominica", "Monday": "Feria II", "Tuesday": "Feria III", "Wednesday": "Feria IV",
           "Thursday": "Feria V", "Friday": "Feria VI", "Saturday": "Sabbato"},
}

UNIT_LABELS = {
    "en": {
        "deus": "Deus in Adiutorium", "hymn": "Hymn", "antiphon": "Antiphon",
        "psalm": "Psalm", "canticle": "Canticle", "reading": "Short Reading",
        "responsory": "Responsory", "gospel_canticle_magnificat": "Gospel Canticle (Magnificat)",
        "gospel_canticle_benedictus": "Gospel Canticle (Benedictus)", "nunc_dimittis": "Canticle (Nunc Dimittis)",
        "intercessions": "Intercessions", "our_father": "Our Father",
        "concluding_prayer": "Concluding Prayer", "dismissal": "Dismissal",
        "missing": "[not yet sourced]", "repeated": "(repeated)",
        "psalmody_gap": "Psalmody",
        "psalmody_gap_note": "This celebration's own proper psalmody for this hour has not been sourced yet "
                              "(a known, tracked gap - not a display error).",
        "vespers_omitted_holy_saturday": "Evening Prayer",
        "vespers_omitted_holy_saturday_note": "Evening Prayer is not celebrated on Holy Saturday: the Easter "
                                               "Vigil takes its place (General Instruction of the Liturgy of the "
                                               "Hours, 208–209). Night Prayer, below, remains for those not "
                                               "attending the Vigil.",
    },
    "es": {
        "deus": "Deus in Adiutorium", "hymn": "Himno", "antiphon": "Antífona",
        "psalm": "Salmo", "canticle": "Cántico", "reading": "Lectura breve",
        "responsory": "Responsorio", "gospel_canticle_magnificat": "Cántico evangélico (Magníficat)",
        "gospel_canticle_benedictus": "Cántico evangélico (Benedictus)", "nunc_dimittis": "Cántico (Nunc dimittis)",
        "intercessions": "Preces", "our_father": "Padre Nuestro",
        "concluding_prayer": "Oración conclusiva", "dismissal": "Despedida",
        "missing": "[pendiente de origen]", "repeated": "(se repite)",
        "psalmody_gap": "Salmodia",
        "psalmody_gap_note": "La salmodia propia de esta celebración para esta hora todavía no ha sido "
                              "recopilada (una carencia conocida y registrada, no un error de la página).",
        "vespers_omitted_holy_saturday": "Vísperas",
        "vespers_omitted_holy_saturday_note": "Las Vísperas no se celebran el Sábado Santo: la Vigilia Pascual "
                                               "ocupa su lugar (Instrucción General de la Liturgia de las Horas, "
                                               "208–209). Las Completas, más abajo, siguen disponibles para "
                                               "quienes no asisten a la Vigilia.",
    },
    "la": {
        "deus": "Deus in Adiutorium", "hymn": "Hymnus", "antiphon": "Antiphona",
        "psalm": "Psalmus", "canticle": "Canticum", "reading": "Lectio brevis",
        "responsory": "Responsorium", "gospel_canticle_magnificat": "Canticum Evangelicum (Magnificat)",
        "gospel_canticle_benedictus": "Canticum Evangelicum (Benedictus)", "nunc_dimittis": "Canticum (Nunc dimittis)",
        "intercessions": "Preces", "our_father": "Pater Noster",
        "concluding_prayer": "Oratio", "dismissal": "Dimissio",
        "missing": "[nondum inventum]", "repeated": "(iteratur)",
        "psalmody_gap": "Psalmodia",
        "psalmody_gap_note": "Psalmodia propria huius celebrationis pro hac hora nondum inventa est "
                              "(defectus cognitus et notatus, non error paginae).",
        "vespers_omitted_holy_saturday": "Vesperae",
        "vespers_omitted_holy_saturday_note": "Sabbato Sancto Vesperae non dicuntur: earum locum Vigilia "
                                               "Paschalis tenet (Institutio Generalis de Liturgia Horarum, "
                                               "208–209). Completorium, infra, iis qui Vigiliae non intersunt "
                                               "manet.",
    },
}

HOUR_LABELS = {
    "en": {"lauds": "Lauds", "vespers": "Vespers", "compline": "Compline",
           "office_of_readings": "Office of Readings", "terce": "Terce", "sext": "Sext", "none_hour": "None"},
    "es": {"lauds": "Laudes", "vespers": "Vísperas", "compline": "Completas",
           "office_of_readings": "Oficio de Lectura", "terce": "Tercia", "sext": "Sexta", "none_hour": "Nona"},
    "la": {"lauds": "Laudes", "vespers": "Vesperae", "compline": "Completorium",
           "office_of_readings": "Officium Lectionis", "terce": "Tertia", "sext": "Sexta", "none_hour": "Nona"},
}

MONTH_NAMES = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    # Classical genitive forms ("die N Augusti" = "the Nth of August"), the
    # standard way a date is stated in Latin - matches how a Kalendarium reads.
    "la": ["Ianuarii", "Februarii", "Martii", "Aprilis", "Maii", "Iunii", "Iulii",
           "Augusti", "Septembris", "Octobris", "Novembris", "Decembris"],
}

# UI chrome (control labels, not liturgical content) - the whole page follows
# whatever language is on the left/"main" side, so every static label needs a
# translation here rather than being hardcoded in one language.
CHROME_LABELS = {
    "en": {"main": "Main", "vernacular": "Vernacular", "translation": "Translation",
           "timezone": "Timezone", "date": "Date", "hour": "Hour", "coming_soon": "(coming soon)"},
    "es": {"main": "Principal", "vernacular": "Vernácula", "translation": "Traducción",
           "timezone": "Zona horaria", "date": "Fecha", "hour": "Hora", "coming_soon": "(próximamente)"},
    "la": {"main": "Principalis", "vernacular": "Vernacula", "translation": "Translatio",
           "timezone": "Zona Temporis", "date": "Dies", "hour": "Hora", "coming_soon": "(nondum)"},
}

# IANA timezone region prefixes (the part before the first "/") translated -
# the specific city/location segment (e.g. "Los_Angeles") has no established
# Latin or Spanish naming convention for the full ~400-entry IANA list, so
# only this recurring, finite set of region words is translated.
TZ_REGION_NAMES = {
    "en": {"Africa": "Africa", "America": "America", "Antarctica": "Antarctica", "Arctic": "Arctic",
           "Asia": "Asia", "Atlantic": "Atlantic", "Australia": "Australia", "Europe": "Europe",
           "Indian": "Indian", "Pacific": "Pacific", "Etc": "Etc"},
    "es": {"Africa": "África", "America": "América", "Antarctica": "Antártida", "Arctic": "Ártico",
           "Asia": "Asia", "Atlantic": "Atlántico", "Australia": "Australia", "Europe": "Europa",
           "Indian": "Índico", "Pacific": "Pacífico", "Etc": "Etc"},
    "la": {"Africa": "Africa", "America": "America", "Antarctica": "Antarctica", "Arctic": "Arcticus",
           "Asia": "Asia", "Atlantic": "Atlanticus", "Australia": "Australia", "Europe": "Europa",
           "Indian": "Indicus", "Pacific": "Pacificus", "Etc": "Etc"},
}


def date_human(d, lang: str) -> str:
    """d: datetime.date. Full localized date string for the page heading and
    the Date picker's option labels - not just the weekday name (day_description
    already handles that for the liturgical meta line)."""
    weekday_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][d.weekday()]
    if lang == "es":
        wd = WEEKDAY_NAMES["es"][weekday_en]
        return f"{wd}, {d.day} de {MONTH_NAMES['es'][d.month - 1]} de {d.year}"
    if lang == "la":
        wd = WEEKDAY_NAMES["la"][weekday_en]
        return f"{wd}, die {d.day} {MONTH_NAMES['la'][d.month - 1]}, anno Domini {d.year}"
    wd = WEEKDAY_NAMES["en"][weekday_en]
    return f"{wd}, {MONTH_NAMES['en'][d.month - 1]} {d.day}, {d.year}"

# Hours actually built vs. placeholders shown-but-disabled in the UI
IMPLEMENTED_HOURS = ["lauds", "vespers", "compline"]
ALL_HOURS_ORDER = ["office_of_readings", "lauds", "terce", "sext", "none_hour", "vespers", "compline"]


def roman_numeral(n: int) -> str:
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for v, sym in vals:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out)


def ordinal_en(n: int) -> str:
    suffix = "th" if 11 <= (n % 100) <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}<sup>{suffix}</sup>"


def ordinal_es(n: int) -> str:
    return f"{n}.<sup>a</sup>"


LATIN_MONTH_GENITIVE = {12: "Decembris"}


def advent_day_description(weekday_en: str, week_number, day_of_month, lang: str, is_sunday: bool = False) -> str:
    """week_number is 1-4 for the regular weeks, None for a December 17-24
    'greater feria' (day_of_month set instead) - see resolver.AdventTag."""
    if week_number is None:
        if lang == "es":
            return f"{day_of_month} de diciembre, Adviento"
        if lang == "la":
            return f"Feria propria diei {day_of_month} {LATIN_MONTH_GENITIVE[12]}, Adventus"
        return f"December {day_of_month}, Advent"

    if is_sunday:
        if lang == "es":
            return f"Domingo {ordinal_es(week_number)} de Adviento"
        if lang == "la":
            return f"Dominica {roman_numeral(week_number)} Adventus"
        return f"{ordinal_en(week_number)} Sunday of Advent"

    if lang == "es":
        wd = WEEKDAY_NAMES["es"][weekday_en]
        return f"{wd} de la {ordinal_es(week_number)} semana de Adviento"
    if lang == "la":
        wd = WEEKDAY_NAMES["la"][weekday_en]
        return f"{wd} hebdomadae {roman_numeral(week_number)} Adventus"
    wd = WEEKDAY_NAMES["en"][weekday_en]
    return f"{wd} of the {ordinal_en(week_number)} Week of Advent"


_LENT_NAMED_DAYS = {
    "ash_wednesday": {"en": "Ash Wednesday", "es": "Miércoles de Ceniza", "la": "Feria IV Cinerum"},
    "thursday_after_ash_wednesday": {"en": "Thursday after Ash Wednesday",
                                      "es": "Jueves después de Ceniza", "la": "Feria V post Cineres"},
    "friday_after_ash_wednesday": {"en": "Friday after Ash Wednesday",
                                    "es": "Viernes después de Ceniza", "la": "Feria VI post Cineres"},
    "saturday_after_ash_wednesday": {"en": "Saturday after Ash Wednesday",
                                      "es": "Sábado después de Ceniza", "la": "Sabbato post Cineres"},
    "palm_sunday_of_the_passion_of_the_lord": {
        "en": "Palm Sunday of the Passion of the Lord",
        "es": "Domingo de Ramos de la Pasión del Señor",
        "la": "Dominica in Palmis de Passione Domini"},
    "holy_monday": {"en": "Monday of Holy Week", "es": "Lunes Santo", "la": "Feria II Hebdomadae Sanctae"},
    "holy_tuesday": {"en": "Tuesday of Holy Week", "es": "Martes Santo", "la": "Feria III Hebdomadae Sanctae"},
    "holy_wednesday": {"en": "Wednesday of Holy Week", "es": "Miércoles Santo", "la": "Feria IV Hebdomadae Sanctae"},
}


_TRIDUUM_NAMED_DAYS = {
    "holy_thursday": {"en": "Holy Thursday of the Lord's Supper",
                       "es": "Jueves Santo, Misa Vespertina de la Cena del Señor",
                       "la": "Feria V in Cena Domini"},
    "friday_of_the_passion_of_the_lord": {"en": "Good Friday of the Lord's Passion",
                                           "es": "Viernes Santo de la Pasión del Señor",
                                           "la": "Feria VI in Passione Domini"},
    "holy_saturday": {"en": "Holy Saturday", "es": "Sábado Santo", "la": "Sabbato Sancto"},
}


def triduum_day_description(breviarium_id: str, lang: str) -> str:
    """See resolver.resolve_triduum - breviarium_id already fully determines
    the day (only 3 possible values, no numbered-week concept here)."""
    return _TRIDUUM_NAMED_DAYS[breviarium_id][lang]


_EASTER_NAMED_DAYS = {
    "easter_sunday": {"en": "Easter Sunday", "es": "Domingo de Pascua de Resurrección", "la": "Dominica Paschae"},
    "easter_monday": {"en": "Monday within the Octave of Easter",
                       "es": "Lunes de la Octava de Pascua", "la": "Feria II infra Octavam Paschae"},
    "easter_tuesday": {"en": "Tuesday within the Octave of Easter",
                        "es": "Martes de la Octava de Pascua", "la": "Feria III infra Octavam Paschae"},
    "easter_wednesday": {"en": "Wednesday within the Octave of Easter",
                          "es": "Miércoles de la Octava de Pascua", "la": "Feria IV infra Octavam Paschae"},
    "easter_thursday": {"en": "Thursday within the Octave of Easter",
                         "es": "Jueves de la Octava de Pascua", "la": "Feria V infra Octavam Paschae"},
    "easter_friday": {"en": "Friday within the Octave of Easter",
                       "es": "Viernes de la Octava de Pascua", "la": "Feria VI infra Octavam Paschae"},
    "easter_saturday": {"en": "Saturday within the Octave of Easter",
                         "es": "Sábado de la Octava de Pascua", "la": "Sabbato infra Octavam Paschae"},
    "divine_mercy_sunday": {"en": "Divine Mercy Sunday (2nd Sunday of Easter)",
                             "es": "Domingo de la Divina Misericordia (2.º de Pascua)",
                             "la": "Dominica II Paschae (de Divina Misericordia)"},
    "ascension_of_the_lord": {"en": "The Ascension of the Lord",
                               "es": "La Ascensión del Señor", "la": "In Ascensione Domini"},
    "pentecost_sunday": {"en": "Pentecost Sunday", "es": "Domingo de Pentecostés", "la": "Dominica Pentecostes"},
    "easter_time_7_sunday": {"en": "7th Sunday of Easter", "es": "7.º Domingo de Pascua",
                              "la": "Dominica VII Paschae"},
}


def easter_day_description(weekday_en: str, week_number, breviarium_id: str, lang: str, is_sunday: bool = False) -> str:
    """week_number is 2-7 for the regular numbered weeks, None for the
    Octave or a named Solemnity (breviarium_id then names the specific
    day) - see resolver.EasterTag."""
    if week_number is None:
        return _EASTER_NAMED_DAYS[breviarium_id][lang]

    if is_sunday:
        if lang == "es":
            return f"Domingo {ordinal_es(week_number)} de Pascua"
        if lang == "la":
            return f"Dominica {roman_numeral(week_number)} Paschae"
        return f"{ordinal_en(week_number)} Sunday of Easter"

    if lang == "es":
        wd = WEEKDAY_NAMES["es"][weekday_en]
        return f"{wd} de la {ordinal_es(week_number)} semana de Pascua"
    if lang == "la":
        wd = WEEKDAY_NAMES["la"][weekday_en]
        return f"{wd} hebdomadae {roman_numeral(week_number)} Temporis Paschalis"
    wd = WEEKDAY_NAMES["en"][weekday_en]
    return f"{wd} of the {ordinal_en(week_number)} Week of Easter"


def christmas_day_description(weekday_en: str, breviarium_id: str, lang: str) -> str:
    """See resolver.resolve_christmas - breviarium_id already fully
    determines the day (there's no numbered-week concept here)."""
    if breviarium_id == "holy_family_of_jesus_mary_and_joseph":
        if lang == "es":
            return "La Sagrada Familia de Jesús, María y José"
        if lang == "la":
            return "Sanctae Familiae Iesu, Mariae et Ioseph"
        return "The Holy Family of Jesus, Mary and Joseph"
    if breviarium_id.startswith("christmas_octave_day_"):
        n = breviarium_id.rsplit("_", 1)[1]
        wd = WEEKDAY_NAMES[lang][weekday_en]
        if lang == "es":
            return f"{wd} de la Octava de Navidad (día {n})"
        if lang == "la":
            return f"{wd} infra Octavam Nativitatis (dies {n})"
        return f"{wd} within the Octave of Christmas (day {n})"
    if breviarium_id == "second_sunday_after_christmas":
        if lang == "es":
            return "II Domingo después de Navidad"
        if lang == "la":
            return "Dominica II post Nativitatem"
        return "2nd Sunday after Christmas"
    if breviarium_id.startswith("christmas_time_january_"):
        n = breviarium_id.rsplit("_", 1)[1]
        wd = WEEKDAY_NAMES[lang][weekday_en]
        if lang == "es":
            return f"{wd} {n} de enero, Tiempo de Navidad"
        if lang == "la":
            return f"{wd}, {n} Ianuarii, Tempus Nativitatis"
        return f"{wd}, January {n}, Christmas Time"
    if breviarium_id.endswith("_after_epiphany"):
        wd = WEEKDAY_NAMES[lang][weekday_en]
        if lang == "es":
            return f"{wd} después de la Epifanía"
        if lang == "la":
            return f"{wd} post Epiphaniam"
        return f"{wd} after Epiphany"
    return breviarium_id


def lent_day_description(weekday_en: str, week_number, breviarium_id: str, lang: str, is_sunday: bool = False) -> str:
    """week_number is 1-5 for the regular numbered weeks, None for the
    pre-Lent-1 days, Palm Sunday, or Holy Week (breviarium_id then names the
    specific day) - see resolver.LentTag."""
    if week_number is None:
        return _LENT_NAMED_DAYS[breviarium_id][lang]

    if is_sunday:
        if lang == "es":
            return f"Domingo {ordinal_es(week_number)} de Cuaresma"
        if lang == "la":
            return f"Dominica {roman_numeral(week_number)} in Quadragesima"
        return f"{ordinal_en(week_number)} Sunday of Lent"

    if lang == "es":
        wd = WEEKDAY_NAMES["es"][weekday_en]
        return f"{wd} de la {ordinal_es(week_number)} semana de Cuaresma"
    if lang == "la":
        wd = WEEKDAY_NAMES["la"][weekday_en]
        return f"{wd} hebdomadae {roman_numeral(week_number)} in Quadragesima"
    wd = WEEKDAY_NAMES["en"][weekday_en]
    return f"{wd} of the {ordinal_en(week_number)} Week of Lent"


def day_description(weekday_en: str, ot_week_number: int, psalter_week: int, lang: str, is_sunday: bool = False) -> str:
    if is_sunday:
        if lang == "es":
            return f"Domingo de la {ordinal_es(ot_week_number)} semana del Tiempo Ordinario (semana {psalter_week} del salterio)"
        if lang == "la":
            return f"Dominica {roman_numeral(ot_week_number)} per annum (hebdomada psalterii {roman_numeral(psalter_week)})"
        return f"{ordinal_en(ot_week_number)} Sunday in Ordinary Time (Psalter week {psalter_week})"

    if lang == "es":
        wd = WEEKDAY_NAMES["es"][weekday_en]
        return f"{wd} de la {ordinal_es(ot_week_number)} semana del Tiempo Ordinario (semana {psalter_week} del salterio)"
    if lang == "la":
        wd = WEEKDAY_NAMES["la"][weekday_en]
        return f"{wd} infra hebdomadam {roman_numeral(ot_week_number)} per annum (hebdomada psalterii {roman_numeral(psalter_week)})"
    wd = WEEKDAY_NAMES["en"][weekday_en]
    return f"{wd} in the {ordinal_en(ot_week_number)} Week in Ordinary Time (Psalter week {psalter_week})"
