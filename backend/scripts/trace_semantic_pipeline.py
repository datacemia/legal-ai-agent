#!/usr/bin/env python3
from __future__ import annotations

import importlib
import inspect
import json
import re
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


MODULE_NAME = (
    "app.services.contract_agent.semantic_source_profile"
)

REPORT_DIR = Path("semantic_audit/architecture_trace")
REPORT_PATH = REPORT_DIR / "semantic_pipeline_trace.json"


SAMPLES = {
    "preemptive_en": (
        "en",
        "The Investor shall have the right to purchase its "
        "pro rata share of any new securities issued by the Company.",
    ),
    "preemptive_fr": (
        "fr",
        "L'Investisseur aura le droit d'acquérir sa quote-part "
        "proportionnelle de tout nouveau titre émis par la Société.",
    ),
    "preemptive_ar": (
        "ar",
        "يحق للمستثمر شراء حصته التناسبية من أي أوراق مالية "
        "جديدة تصدرها الشركة.",
    ),
    "appointment_en": (
        "en",
        "The board shall include one director designated by "
        "the Investor.",
    ),
    "tag_en": (
        "en",
        "The Investor shall have the right to participate in "
        "such sale on the same terms.",
    ),
    "consent_en": (
        "en",
        "The Company shall not incur indebtedness without the "
        "Investor's prior written consent.",
    ),
}


def to_json_safe(value: Any) -> Any:
    if value is None or isinstance(
        value,
        (str, int, float, bool),
    ):
        return value

    if isinstance(value, dict):
        return {
            str(key): to_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [
            to_json_safe(item)
            for item in value
        ]

    if hasattr(value, "model_dump"):
        try:
            return to_json_safe(value.model_dump())
        except Exception:
            pass

    if hasattr(value, "dict"):
        try:
            return to_json_safe(value.dict())
        except Exception:
            pass

    if hasattr(value, "__dict__"):
        try:
            return to_json_safe(vars(value))
        except Exception:
            pass

    return repr(value)


def mechanism_names(profile: Any) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}

    if not isinstance(profile, dict):
        return result

    for key in (
        "ranked_material_mechanisms",
        "material_mechanisms",
        "mechanisms",
        "relations",
        "normalized_legal_relations",
    ):
        values = profile.get(key)

        if not isinstance(values, list):
            continue

        names = []

        for value in values:
            if isinstance(value, dict):
                names.append(
                    str(
                        value.get("kind")
                        or value.get("concept")
                        or value.get("type")
                        or value.get("semantic_role")
                        or "<dict>"
                    )
                )
            else:
                names.append(str(value))

        result[key] = names

    return result


def find_symbol_occurrences(
    root: Path,
    symbols: set[str],
) -> list[dict[str, Any]]:
    occurrences = []

    for path in sorted(root.rglob("*.py")):
        try:
            lines = path.read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines()
        except OSError:
            continue

        for number, line in enumerate(lines, start=1):
            matched = [
                symbol
                for symbol in symbols
                if symbol in line
            ]

            if matched:
                occurrences.append({
                    "file": str(path),
                    "line": number,
                    "symbols": matched,
                    "text": line.strip(),
                })

    return occurrences


def main() -> int:
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    importlib.invalidate_caches()
    module = importlib.import_module(MODULE_NAME)

    function = getattr(
        module,
        "build_semantic_source_profile",
        None,
    )

    if function is None:
        print(
            "ERROR: build_semantic_source_profile "
            "not found"
        )
        return 1

    module_file = Path(
        inspect.getsourcefile(module)
        or module.__file__
    ).resolve()

    function_file = inspect.getsourcefile(function)

    try:
        function_source = inspect.getsource(function)
    except Exception as exc:
        function_source = (
            f"<source unavailable: "
            f"{type(exc).__name__}: {exc}>"
        )

    module_text = module_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    runtime = {
        "repository_root": str(REPOSITORY_ROOT),
        "module_name": MODULE_NAME,
        "module_file": str(module_file),
        "module_cached": getattr(
            module,
            "__cached__",
            None,
        ),
        "function_module": getattr(
            function,
            "__module__",
            None,
        ),
        "function_qualname": getattr(
            function,
            "__qualname__",
            None,
        ),
        "function_signature": str(
            inspect.signature(function)
        ),
        "function_file": function_file,
        "function_line": (
            inspect.getsourcelines(function)[1]
            if function_file
            else None
        ),
        "function_source": function_source,
        "patch_marker_present": (
            "BEGIN PATCH HIGH_FAILURES_MULTILANG_V1"
            in module_text
        ),
        "patch_original_in_globals": (
            "_hf_original_build_semantic_source_profile"
            in getattr(function, "__globals__", {})
        ),
        "build_definition_count": len(
            re.findall(
                r"(?m)^def\s+"
                r"build_semantic_source_profile\s*\(",
                module_text,
            )
        ),
        "module_line_count": len(
            module_text.splitlines()
        ),
        "module_tail": module_text.splitlines()[-80:],
    }

    samples = {}

    for name, (language, text) in SAMPLES.items():
        entry: dict[str, Any] = {
            "language": language,
            "text": text,
        }

        try:
            profile = function(
                text,
                language=language,
            )

            safe_profile = to_json_safe(profile)

            entry["result_type"] = type(profile).__name__
            entry["top_level_keys"] = (
                sorted(safe_profile)
                if isinstance(safe_profile, dict)
                else []
            )
            entry["mechanisms"] = mechanism_names(
                safe_profile
            )
            entry["profile"] = safe_profile

        except Exception as exc:
            entry["error"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }

        samples[name] = entry

    symbols = {
        "build_semantic_source_profile",
        "TAG_ALONG_RIGHT",
        "PREEMPTIVE_RIGHT",
        "APPOINTMENT_RIGHT",
        "PARTICIPATION_OPTION",
        "SAME_TERMS_RIGHT",
        "INVESTOR_CONSENT_RIGHT",
        "RESERVED_MATTER",
        "CONSENT_PREREQUISITE",
        "BOARD_COMPOSITION",
        "ranked_material_mechanisms",
        "material_mechanisms",
    }

    report = {
        "runtime": runtime,
        "samples": samples,
        "occurrences": find_symbol_occurrences(
            Path("app/services/contract_agent"),
            symbols,
        ),
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    print("=" * 78)
    print("SEMANTIC PIPELINE TRACE")
    print("=" * 78)
    print("REPOSITORY ROOT :", REPOSITORY_ROOT)
    print("MODULE FILE     :", module_file)
    print("FUNCTION FILE   :", function_file)
    print("FUNCTION LINE   :", runtime["function_line"])
    print(
        "FUNCTION        :",
        runtime["function_qualname"],
    )
    print(
        "SIGNATURE       :",
        runtime["function_signature"],
    )
    print(
        "PATCH MARKER    :",
        runtime["patch_marker_present"],
    )
    print(
        "PATCH GLOBAL    :",
        runtime["patch_original_in_globals"],
    )
    print(
        "BUILD DEF COUNT :",
        runtime["build_definition_count"],
    )
    print("REPORT          :", REPORT_PATH)

    print("\nSAMPLE OUTPUTS")

    for name, entry in samples.items():
        print("-" * 78)
        print(name)

        if "error" in entry:
            print("ERROR:", entry["error"])
            continue

        print("TYPE:", entry["result_type"])
        print("KEYS:", entry["top_level_keys"])

        for key, values in entry["mechanisms"].items():
            print(f"{key}:", values)

    print("\nRELEVANT SOURCE OCCURRENCES")

    for item in report["occurrences"]:
        print(
            f"{item['file']}:{item['line']}",
            f"[{', '.join(item['symbols'])}]",
        )
        print(" ", item["text"])

    print("\nRUNTIME FUNCTION SOURCE")
    print("-" * 78)
    print(function_source)

    print("\nLAST 80 LINES OF IMPORTED MODULE")
    print("-" * 78)

    start = max(
        1,
        runtime["module_line_count"] - 79,
    )

    for index, line in enumerate(
        runtime["module_tail"],
        start=start,
    ):
        print(f"{index:>5}: {line}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
