from __future__ import annotations

import csv
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


INPUT_DIR = Path("semantic_audit")
OUTPUT_DIR = INPUT_DIR / "human_signoff"

EXPECTED_TOTAL = 105
EXPECTED_COUNTS = Counter({
    "en": 35,
    "fr": 35,
    "ar": 35,
})

TEXT_KEYS = (
    "clause_text",
    "source_text",
    "text",
    "clause",
    "sentence",
    "content",
)

LANGUAGE_KEYS = (
    "language",
    "lang",
    "locale",
)

ID_KEYS = (
    "clause_id",
    "gold_id",
    "case_id",
    "record_id",
    "id",
)

PRIMARY_TYPE_KEYS = (
    "expected_primary_type",
    "gold_primary_type",
    "primary_type",
)

CONCEPT_KEYS = (
    "expected_concept",
    "gold_concept",
    "normalized_concept",
    "concept",
)

RELATION_KEYS = (
    "expected_relation",
    "gold_relation",
    "normalized_relation",
    "relation",
)

GOLD_CONTAINER_KEYS = (
    "expected",
    "gold",
    "reference",
    "target",
    "annotation",
    "labels",
)


def safe_string(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
    )


def first_value(
    mapping: dict[str, Any],
    keys: Iterable[str],
) -> Any:
    for key in keys:
        value = mapping.get(key)

        if value not in (None, "", [], {}):
            return value

    return None


def normalize_language(
    value: Any,
    text: str,
) -> str:
    raw = safe_string(value).lower()

    aliases = {
        "english": "en",
        "anglais": "en",
        "en-us": "en",
        "en-gb": "en",
        "french": "fr",
        "français": "fr",
        "francais": "fr",
        "fr-fr": "fr",
        "arabic": "ar",
        "arabe": "ar",
        "العربية": "ar",
        "ar-sa": "ar",
        "ar-ma": "ar",
    }

    normalized = aliases.get(raw, raw)

    if normalized in {"en", "fr", "ar"}:
        return normalized

    if any("\u0600" <= char <= "\u06ff" for char in text):
        return "ar"

    lowered = text.lower()

    french_markers = (
        "la société",
        "le présent",
        "l'investisseur",
        "ne peut",
        "devra",
        "conformément",
        "résiliation",
        "préavis",
        "cession",
        "sous réserve",
    )

    if any(marker in lowered for marker in french_markers):
        return "fr"

    return "en"


def gold_container(
    record: dict[str, Any],
) -> dict[str, Any]:
    for key in GOLD_CONTAINER_KEYS:
        value = record.get(key)

        if isinstance(value, dict):
            return value

    return record


def extract_relation(
    container: dict[str, Any],
) -> dict[str, Any]:
    relation = first_value(
        container,
        RELATION_KEYS,
    )

    if isinstance(relation, dict):
        return relation

    return {}


def looks_like_gold_record(
    record: dict[str, Any],
) -> bool:
    text = first_value(
        record,
        TEXT_KEYS,
    )

    if not isinstance(text, str):
        return False

    if len(text.strip()) < 15:
        return False

    container = gold_container(record)

    has_primary = (
        first_value(
            container,
            PRIMARY_TYPE_KEYS,
        )
        is not None
    )

    has_concept = (
        first_value(
            container,
            CONCEPT_KEYS,
        )
        is not None
    )

    has_relation = isinstance(
        first_value(
            container,
            RELATION_KEYS,
        ),
        dict,
    )

    return sum(
        (
            has_primary,
            has_concept,
            has_relation,
        )
    ) >= 2


def walk_records(
    value: Any,
    path: str = "$",
) -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        if looks_like_gold_record(value):
            yield path, value
            return

        for key, child in value.items():
            yield from walk_records(
                child,
                f"{path}.{key}",
            )

    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_records(
                child,
                f"{path}[{index}]",
            )


def record_identity(
    record: dict[str, Any],
) -> tuple[str, str, str]:
    text = safe_string(
        first_value(
            record,
            TEXT_KEYS,
        )
    )

    language = normalize_language(
        first_value(
            record,
            LANGUAGE_KEYS,
        ),
        text,
    )

    record_id = safe_string(
        first_value(
            record,
            ID_KEYS,
        )
    )

    return (
        language,
        record_id,
        " ".join(text.split()),
    )


def deduplicate(
    records: list[tuple[str, dict[str, Any]]],
) -> list[tuple[str, dict[str, Any]]]:
    output: list[
        tuple[str, dict[str, Any]]
    ] = []

    seen: set[
        tuple[str, str, str]
    ] = set()

    for path, record in records:
        identity = record_identity(record)

        if identity in seen:
            continue

        seen.add(identity)
        output.append((path, record))

    return output


def count_languages(
    records: list[tuple[str, dict[str, Any]]],
) -> Counter[str]:
    counts: Counter[str] = Counter()

    for _, record in records:
        language, _, _ = record_identity(record)
        counts[language] += 1

    return counts


def find_candidates() -> list[
    tuple[
        Path,
        list[tuple[str, dict[str, Any]]],
    ]
]:
    exact_candidates: list[
        tuple[
            Path,
            list[tuple[str, dict[str, Any]]],
        ]
    ] = []

    diagnostics: list[
        tuple[
            Path,
            int,
            Counter[str],
        ]
    ] = []

    for json_file in sorted(
        INPUT_DIR.rglob("*.json")
    ):
        if OUTPUT_DIR in json_file.parents:
            continue

        try:
            payload = json.loads(
                json_file.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
        ):
            continue

        records = deduplicate(
            list(walk_records(payload))
        )

        if not records:
            continue

        counts = count_languages(records)

        diagnostics.append(
            (
                json_file,
                len(records),
                counts,
            )
        )

        if (
            len(records) == EXPECTED_TOTAL
            and counts == EXPECTED_COUNTS
        ):
            exact_candidates.append(
                (
                    json_file,
                    records,
                )
            )

    if exact_candidates:
        print("EXACT CANDIDATES:")

        for json_file, records in exact_candidates:
            print(
                f"  - {json_file}: "
                f"{len(records)} "
                f"{dict(count_languages(records))}"
            )

        return exact_candidates

    print(
        "ERROR: aucun fichier JSON exact "
        "de 105 clauses trouvé.",
        file=sys.stderr,
    )

    print(
        "MEILLEURS CANDIDATS:",
        file=sys.stderr,
    )

    ranked = sorted(
        diagnostics,
        key=lambda item: (
            abs(item[1] - EXPECTED_TOTAL),
            abs(item[2].get("en", 0) - 35)
            + abs(item[2].get("fr", 0) - 35)
            + abs(item[2].get("ar", 0) - 35),
        ),
    )

    for json_file, total, counts in ranked[:20]:
        print(
            f"  - {json_file}: "
            f"total={total}, "
            f"languages={dict(counts)}",
            file=sys.stderr,
        )

    return []


def build_row(
    index: int,
    source_file: Path,
    source_path: str,
    record: dict[str, Any],
) -> dict[str, Any]:
    text = safe_string(
        first_value(
            record,
            TEXT_KEYS,
        )
    )

    language = normalize_language(
        first_value(
            record,
            LANGUAGE_KEYS,
        ),
        text,
    )

    record_id = safe_string(
        first_value(
            record,
            ID_KEYS,
        )
    )

    if not record_id:
        record_id = (
            f"GOLD-{language.upper()}-{index:03d}"
        )

    container = gold_container(record)
    relation = extract_relation(container)

    return {
        "review_index": index,
        "source_file": str(source_file),
        "source_path": source_path,
        "record_id": record_id,
        "language": language,
        "clause_text": text,
        "gold_primary_type": safe_string(
            first_value(
                container,
                PRIMARY_TYPE_KEYS,
            )
        ),
        "gold_normalized_concept": safe_string(
            first_value(
                container,
                CONCEPT_KEYS,
            )
        ),
        "gold_right_holder": safe_string(
            relation.get("right_holder")
        ),
        "gold_obligated_actor": safe_string(
            relation.get("obligated_actor")
        ),
        "gold_counterparty": safe_string(
            relation.get("counterparty")
        ),
        "gold_beneficiary": safe_string(
            relation.get("beneficiary")
        ),
        "gold_object": safe_string(
            relation.get("object")
        ),
        "gold_trigger": safe_string(
            relation.get("trigger")
        ),
        "gold_action": safe_string(
            relation.get("action")
        ),
        "gold_polarity": safe_string(
            relation.get("polarity")
        ),
        "gold_procedural_states": safe_string(
            relation.get(
                "procedural_states",
                [],
            )
        ),
        "gold_numeric_semantic_roles": safe_string(
            relation.get(
                "numeric_semantic_roles",
                [],
            )
        ),
        "decision": "PENDING",
        "reviewer": "",
        "review_date": "",
        "grounding_status": "",
        "correction_primary_type": "",
        "correction_normalized_concept": "",
        "correction_relation_json": "",
        "reviewer_comment": "",
    }


def write_package(
    source_file: Path,
    records: list[tuple[str, dict[str, Any]]],
) -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=False,
    )

    ordered = sorted(
        records,
        key=lambda item: record_identity(
            item[1]
        ),
    )

    rows = [
        build_row(
            index,
            source_file,
            path,
            record,
        )
        for index, (path, record) in enumerate(
            ordered,
            start=1,
        )
    ]

    csv_path = (
        OUTPUT_DIR
        / "gold_human_signoff.csv"
    )

    jsonl_path = (
        OUTPUT_DIR
        / "gold_human_signoff.jsonl"
    )

    manifest_path = (
        OUTPUT_DIR
        / "signoff_manifest.json"
    )

    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
        )
        writer.writeheader()
        writer.writerows(rows)

    with jsonl_path.open(
        "w",
        encoding="utf-8",
    ) as handle:
        for row in rows:
            handle.write(
                json.dumps(
                    row,
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )

    manifest = {
        "status": "PENDING_HUMAN_SIGNOFF",
        "source_file": str(source_file),
        "total_records": len(rows),
        "language_counts": dict(
            Counter(
                row["language"]
                for row in rows
            )
        ),
        "expected_total": EXPECTED_TOTAL,
        "expected_language_counts": dict(
            EXPECTED_COUNTS
        ),
        "allowed_decisions": [
            "ACCEPT",
            "CORRECT",
            "REJECT",
            "ESCALATE",
        ],
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "FROZEN GOLD SIGNOFF PACKAGE CREATED"
    )
    print(f"SOURCE    : {source_file}")
    print(f"RECORDS   : {len(rows)}")
    print(
        "LANGUAGES :",
        dict(
            Counter(
                row["language"]
                for row in rows
            )
        ),
    )
    print(f"CSV       : {csv_path}")
    print(f"JSONL     : {jsonl_path}")
    print(f"MANIFEST  : {manifest_path}")


def main() -> int:
    if not INPUT_DIR.is_dir():
        print(
            f"ERROR: dossier absent: {INPUT_DIR}",
            file=sys.stderr,
        )
        return 1

    candidates = find_candidates()

    if not candidates:
        return 2

    if len(candidates) > 1:
        print()
        print(
            "ERROR: plusieurs corpus exacts ont "
            "été trouvés.",
            file=sys.stderr,
        )
        print(
            "Aucun package n’a été créé afin "
            "d’éviter de choisir le mauvais corpus.",
            file=sys.stderr,
        )
        return 3

    source_file, records = candidates[0]

    write_package(
        source_file,
        records,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
