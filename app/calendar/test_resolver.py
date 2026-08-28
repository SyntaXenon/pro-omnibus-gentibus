from datetime import date
from resolver import (
    easter_sunday, ash_wednesday, pentecost, baptism_of_the_lord,
    first_sunday_of_advent, resolve_ferial_ordinary_time,
)

# Well-known Easter dates, used to validate the Computus implementation.
KNOWN_EASTER = {
    2023: date(2023, 4, 9),
    2024: date(2024, 3, 31),
    2025: date(2025, 4, 20),
    2026: date(2026, 4, 5),
    2027: date(2027, 3, 28),
    2028: date(2028, 4, 16),
}

failures = []
for year, expected in KNOWN_EASTER.items():
    got = easter_sunday(year)
    status = "OK" if got == expected else "FAIL"
    if got != expected:
        failures.append(year)
    print(f"Easter {year}: got {got}, expected {expected} [{status}]")

print()
for year in KNOWN_EASTER:
    print(f"{year}: Easter={easter_sunday(year)} AshWed={ash_wednesday(year)} "
          f"Pentecost={pentecost(year)} Baptism={baptism_of_the_lord(year)} "
          f"Advent1={first_sunday_of_advent(year)}")

print()
print("Sample ferial resolutions:")
samples = [
    date(2026, 1, 12),   # Monday after Baptism of the Lord 2026 -> should be OT week 1
    date(2026, 7, 30),   # a Thursday in mid-year Ordinary Time Part 2, 2026
    date(2026, 11, 21),  # Saturday of the week before the last OT week of 2026 -> should be week 33
    date(2026, 2, 20),   # during Lent -> should be None (out of scope)
]
for d in samples:
    tag = resolve_ferial_ordinary_time(d)
    print(f"{d} ({d.strftime('%A')}): {tag}")

print()
if failures:
    print(f"EASTER COMPUTUS FAILURES: {failures}")
else:
    print("All Easter dates matched known values.")
