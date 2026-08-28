# -*- coding: utf-8 -*-
"""Resolves breviarium-core day-index entries (all_laudes.json, all_vesperae.json,
etc. - numeric-id fields) against the databases/es/commons/*.json lookup tables,
mirroring src/prayers/mappers/findText/index.ts's simple id->val lookup.

Source: https://github.com/Breviarium-app/breviarium--core (Apache-2.0/MIT,
see NOTICE for attribution requirement). Cached locally under
_external_sources/breviarium_core/. See memory note "main extract sources"
for the full field/table map and what each file contains.
"""
import json
from pathlib import Path
from functools import lru_cache

ROOT = Path(r"C:\Omnium Gentium LOTH\_external_sources\breviarium_core")

# field name (as it appears in an all_*.json day entry) -> commons table name
FIELD_TO_TABLE = {
    "himno": "himnos",
    "himno_latino": "himnos_latinos",
    "primer_salmo_cita": "salmos_citas",
    "primer_salmo_antifona": "salmos_antifonas",
    "primer_salmo_texto": "salmos_textos",
    "segundo_salmo_cita": "salmos_citas",
    "segundo_salmo_antifona": "salmos_antifonas",
    "segundo_salmo_texto": "salmos_textos",
    "tercer_salmo_cita": "salmos_citas",
    "tercer_salmo_antifona": "salmos_antifonas",
    "tercer_salmo_texto": "salmos_textos",
    "lectura_biblica_cita": "lectura_breve_citas",
    "lectura_biblica": "lectura_breve_textos",
    "responsorios": "responsorios",  # array
    "cantico_evangelico_antifona": "cantico_evangelico_antifonas",
    "preces_intro": "preces_intro",
    "preces_respuesta": "preces_respuesta",
    "preces_contenido": "preces_contenido",  # array
    "invitacion_padrenuestro": "invitacion_padrenuestro",
    "oracion_final": "oraciones_finales",
    # Office of Readings (all_officium.json) specific fields
    "lectura_biblica_titulo_a": None,  # literal text already, not an id
    "lectura_biblica_cita_a": "lecturas_referencia",
    "lectura_biblica_texto_a": "lecturas_texto",
    "lectura_patristica_titulo_a": "oficio_titulos",
    "lectura_patristica_cita_a": "oficio_citas",
    "lectura_patristica_texto_a": "oficio_textos",
    "responsorio1": "responsorios",
    "responsorio2_a": "responsorios",
    "responsorio3_a": "responsorios",
}


@lru_cache(maxsize=None)
def _load_day_index(name: str) -> list:
    return json.loads((ROOT / "day_index" / f"{name}.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _load_table(name: str) -> dict:
    raw = json.loads((ROOT / "commons" / f"{name}.json").read_text(encoding="utf-8"))
    return {entry["id"]: entry["val"] for entry in raw}


def find_text(table: str, id_val):
    if id_val is None or table is None:
        return None
    table_data = _load_table(table)
    val = table_data.get(id_val)
    if not val:
        return None
    if "Not found" in val or "Responsorio no encontrado" in val:
        return None
    return val


def get_entry(day_index_name: str, entry_id: str) -> dict:
    """day_index_name: 'all_laudes' | 'all_vesperae' | 'all_officium' | 'all_tertia'
    | 'all_sexta' | 'all_nona' | 'all_invitatorium'. Returns the raw (unresolved)
    entry dict for the given slug id, or None if not present."""
    for entry in _load_day_index(day_index_name):
        if entry.get("id") == entry_id:
            return entry
    return None


def resolve_entry(entry: dict) -> dict:
    """Resolves every id-bearing field in a raw day-entry to its literal text.
    Fields not in FIELD_TO_TABLE (id, cycle, primeras_visperas, etc.) pass through."""
    out = {}
    for key, val in entry.items():
        table = FIELD_TO_TABLE.get(key, "__passthrough__")
        if table == "__passthrough__":
            out[key] = val
        elif table is None:
            out[key] = val
        elif isinstance(val, list):
            resolved = [find_text(table, v) for v in val]
            out[key] = [r for r in resolved if r]
        else:
            out[key] = find_text(table, val)
    return out


def get_resolved(day_index_name: str, entry_id: str) -> dict:
    entry = get_entry(day_index_name, entry_id)
    if entry is None:
        return None
    return resolve_entry(entry)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for name, eid in [("all_laudes", "advent_1_friday"), ("all_vesperae", "advent_1_friday")]:
        r = get_resolved(name, eid)
        print(f"=== {name} / {eid} ===")
        print(json.dumps(r, ensure_ascii=False, indent=2)[:1500])
        print()
