"""
Load the NSW Bird Atlassers CSV exports into Polars, typed per the data dictionary.

Strategy (why this can't hit a ComputeError on read):
  1. Read every column as text (no type guessing at all).
  2. Cast the columns the dictionary defines as integers / dates.
     - Integers go text -> Float64 -> Int64, so values like "2855.0" work.
       (pandas writes nullable int columns as floats, which is where "2855.0" came from.)
  3. Report any value that couldn't be converted, instead of silently dropping it.

Column names are matched loosely (case, spaces, hyphens and underscores ignored),
so "Sp-No", "Sp_No" and "sp_no" all match. Columns not listed below stay as text.
"""

import re
import polars as pl

NULLS = ["NA", ""]


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


# Integer and date columns per table (from the data dictionary).
# Everything else (varchar / text) is kept as text.
SCHEMAS = {
    "header": {
        "int": ["s_ID", "s_Atlasser", "k_Latitude", "k_Longitude",
                "Observation_count", "confidence_Level", "is_Collection"],
        "date": ["s_StartF", "s_DateL"],
    },
    "location": {
        "int": ["bl_ID", "bl_Lat", "bl_Lon", "header_count", "Min_Alt", "Max_Alt"],
    },
    "observation": {
        "int": ["sd_ID", "sd_SpeciesORIG", "sd_breeding", "confidence_Level"],
    },
    "species": {
        "int": ["BLT-sort", "Num-sort", "observation_count"],
        # Sp-No and IOC_Species_ID are varchar in the dictionary -> kept as text
    },
    "ebird": {
        "int": ["Survey ID", "Collection flag", "Observer Id", "Species ID",
                "K-Latitude", "K-Longitude"],
        "date": ["Observation Start Date", "Observation End Date"],
    },
    "synonyms": {},                       # all varchar
    "traits": {"int": ["ID"]},            # everything else is varchar/text
}


def read_table(path: str, table: str) -> pl.DataFrame:
    raw = pl.read_csv(path, infer_schema=False, null_values=NULLS)  # all columns as text

    spec = SCHEMAS[table]
    lookup = {_norm(c): c for c in raw.columns}
    exprs, targets = [], []

    for kind in ("int", "date"):
        for wanted in spec.get(kind, []):
            col = lookup.get(_norm(wanted))
            if col is None:
                print(f"[{table}] note: column '{wanted}' not found in {path}")
                continue
            e = pl.col(col).str.strip_chars()
            if kind == "int":
                e = e.cast(pl.Float64, strict=False).cast(pl.Int64, strict=False)
            else:
                e = e.str.to_date(strict=False)   # format inferred (yyyy-mm-dd or yyyy/mm/dd)
            exprs.append(e.alias(col))
            targets.append(col)

    typed = raw.with_columns(exprs)

    # Report values that were present as text but failed to convert
    for col in targets:
        lost = raw.filter(pl.col(col).is_not_null() & typed[col].is_null())
        if lost.height:
            examples = lost[col].unique().head(5).to_list()
            print(f"[{table}] WARNING: {lost.height:,} values in '{col}' "
                  f"could not be converted, e.g. {examples}")

    return typed


if __name__ == "__main__":
    ebird        = read_table("data/ebird.csv", "ebird")
    observations = read_table("data/observation.csv", "observation")
    species      = read_table("data/899_Species.csv", "species")
    header_df    = read_table("data/header.csv", "header")
    locations    = read_table("data/location.csv", "location")
    traits       = read_table("data/traits.csv", "traits")
    synonyms     = read_table("data/synonyms.csv", "synonyms")