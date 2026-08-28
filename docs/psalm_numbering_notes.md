# Psalm numbering: Hebrew vs. Vulgate, and how it's handled here

Two official Vatican Latin texts use opposite psalm-numbering conventions:
- The **Nova Vulgata** (1979, the Church's official complete Bible) numbers the Psalms
  by the Hebrew/Masoretic convention.
- The **Liber Psalmorum / Liturgia Horarum's own printed psalter** (1969-71, what's
  actually prayed from) numbers the Psalms by the old (Vulgate/Septuagint) convention.

This project treats **old Vulgate numbering as canonical** for all citations,
since that's what matches the actual liturgical books. Any source using Hebrew
numbering gets converted once at ingestion.

## The conversion
- Psalms 1-8: identical in both systems.
- Hebrew 9 and 10 -> combined into Vulgate 9.
- Hebrew 11-113 -> Vulgate = Hebrew number minus 1.
- Hebrew 114 and 115 -> combined into Vulgate 113.
- Hebrew 116 -> splits into Vulgate 114 (roughly its first 9 verses) and Vulgate 115
  (the rest, renumbered).
- Hebrew 117-146 -> Vulgate = Hebrew number minus 1.
- Hebrew 147 -> splits into Vulgate 146 (roughly its first 11 verses) and Vulgate 147
  (the rest, renumbered).
- Hebrew 148-150: identical in both systems.

## What's been converted so far
`content/tables/ferial_psalter_distribution.json` has been converted from a
Hebrew-numbered source. Only two entries in that table actually fell in the
tricky split zones: Hebrew Ps 147 (appears twice, already conveniently split
as "147:1-11" / "147:12-20" in the source, mapped to Vulgate "146:1-11" /
"147:1-9") and Hebrew Ps 116:1-9 (mapped cleanly to the whole of Vulgate
Psalm 114, since that citation happens to be exactly the first-half split).
Hebrew 9/10 and 113/114/115 did not appear anywhere in the ferial Lauds/
Vespers/Compline tables, so that part of the conversion logic is untested -
flag this if a later phase (Sundays, feasts) needs one of those psalms.

**Not yet done:** verifying the converted table against an actual printed
Liturgia Horarum. Treat the two split-case conversions especially as unverified
until checked.
