#!/usr/bin/env python3
from __future__ import annotations

import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Any, Callable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


MODULE_NAME = (
    "app.services.contract_agent.semantic_source_profile"
)

REPORT_DIR = Path("semantic_audit/architecture_trace")
REPORT_PATH = REPORT_DIR / "high_failure_detector_trace.json"


DETECTORS = {
    "preemptive": "_hf_detect_preemptive_right",
    "appointment": "_hf_detect_appointment_right",
    "tag_participation": "_hf_detect_tag_participation",
    "reserved_consent": "_hf_detect_reserved_matter_consent",
}


SAMPLES = {
    "preemptive_en": (
        "preemptive",
        "en",
        "The Investor shall have the right to purchase its "
        "pro rata share of any new securities issued by the Company.",
    ),
    "preemptive_fr": (
        "preemptive",
        "fr",
        "L'Investisseur aura le droit d'acquérir sa quote-part "
        "proportionnelle de tout nouveau titre émis par la Société.",
    ),
    "preemptive_ar": (
        "preemptive",
        "ar",
        "يحق للمستثمر شراء حصته التناسبية من أي أوراق مالية "
        "جديدة تصدرها الشركة.",
    ),
    "appointment_en": (
        "appointment",
        "en",
        "The board shall include one director designated by "
        "the Investor.",
    ),
    "appointment_fr": (
        "appointment",
        "fr",
        "Le conseil d'administration comprendra un administrateur "
        "désigné par l'Investisseur.",
    ),
    "appointment_ar": (
        "appointment",
        "ar",
        "يتضمن مجلس الإدارة عضواً واحداً يعينه المستثمر.",
    ),
    "tag_en": (
        "tag_participation",
        "en",
        "The Investor shall have the right to participate in "
        "such sale on the same terms.",
    ),
    "tag_fr": (
        "tag_participation",
        "fr",
        "L'Investisseur aura le droit de participer à cette "
        "vente aux mêmes conditions.",
    ),
    "tag_ar": (
        "tag_participation",
        "ar",
        "يحق للمستثمر المشاركة في هذا البيع بالشروط نفسها.",
    ),
    "consent_en": (
        "reserved_consent",
        "en",
        "The Company shall not incur indebtedness without the "
        "Investor's prior written consent.",
    ),
    "consent_fr": (
        "reserved_consent",
        "fr",
        "La Société ne pourra contracter aucune dette sans le "
        "consentement écrit préalable de l'Investisseur.",
    ),
    "consent_ar": (
        "reserved_consent",
        "ar",
        "لا يجوز للشركة تحمل أي مديونية دون موافقة كتابية "
        "مسبقة من المستثمر.",
    ),
}


def json_safe(value: Any) -> Any:
    if value is None or isinstance(
        value,
        (str, int, float, bool),
    ):
        return value

    if isinstance(value, dict):
        return {
            str(key): json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [json_safe(item) for item in value]

    return repr(value)


def compact_locals(
    local_values: dict[str, Any],
) -> dict[str, Any]:
    result = {}

    for key, value in local_values.items():
        if key.startswith("__"):
            continue

        safe = json_safe(value)
        rendered = repr(safe)

        if len(rendered) > 600:
            rendered = rendered[:600] + "...<truncated>"

        result[key] = rendered

    return result


def execute_with_trace(
    function: Callable[..., Any],
    text: str,
    language: str,
) -> dict[str, Any]:
    function_code = function.__code__
    events: list[dict[str, Any]] = []

    def tracer(frame, event, arg):
        if frame.f_code is not function_code:
            return tracer

        if event == "line":
            events.append({
                "event": "line",
                "line": frame.f_lineno,
                "locals": compact_locals(
                    dict(frame.f_locals)
                ),
            })

        elif event == "return":
            events.append({
                "event": "return",
                "line": frame.f_lineno,
                "return_value": json_safe(arg),
                "locals": compact_locals(
                    dict(frame.f_locals)
                ),
            })

        elif event == "exception":
            exc_type, exc_value, _ = arg

            events.append({
                "event": "exception",
                "line": frame.f_lineno,
                "exception_type": exc_type.__name__,
                "exception": str(exc_value),
                "locals": compact_locals(
                    dict(frame.f_locals)
                ),
            })

        return tracer

    signature = inspect.signature(function)
    parameters = signature.parameters

    call_attempts = []

    if "language" in parameters:
        call_attempts.append(
            lambda: function(text, language=language)
        )

    call_attempts.extend([
        lambda: function(text),
        lambda: function(
            source_text=text,
            language=language,
        ),
        lambda: function(source_text=text),
    ])

    result: Any = None
    error: Exception | None = None
    successful_call = None

    previous_trace = sys.gettrace()

    try:
        sys.settrace(tracer)

        for index, attempt in enumerate(call_attempts, start=1):
            try:
                result = attempt()
                successful_call = index
                error = None
                break
            except TypeError as exc:
                error = exc
                continue
    finally:
        sys.settrace(previous_trace)

    if successful_call is None:
        return {
            "error": {
                "type": (
                    type(error).__name__
                    if error is not None
                    else "UnknownError"
                ),
                "message": (
                    str(error)
                    if error is not None
                    else "No call attempt succeeded"
                ),
            },
            "events": events,
        }

    return {
        "successful_call_attempt": successful_call,
        "result": json_safe(result),
        "truthy": bool(result),
        "events": events,
    }


def source_with_numbers(
    function: Callable[..., Any],
) -> list[dict[str, Any]]:
    lines, start_line = inspect.getsourcelines(function)

    return [
        {
            "line": start_line + offset,
            "text": line.rstrip("\n"),
        }
        for offset, line in enumerate(lines)
    ]


def print_trace_summary(
    sample_name: str,
    detector_name: str,
    entry: dict[str, Any],
) -> None:
    print("=" * 90)
    print("SAMPLE  :", sample_name)
    print("DETECTOR:", detector_name)

    if "error" in entry:
        print("ERROR   :", entry["error"])
        return

    print("RESULT  :", repr(entry["result"]))
    print("TRUTHY  :", entry["truthy"])

    return_events = [
        event
        for event in entry["events"]
        if event["event"] == "return"
    ]

    if return_events:
        final_event = return_events[-1]
        print("RETURN LINE:", final_event["line"])
        print("FINAL LOCALS:")

        for key, value in final_event["locals"].items():
            print(f"  {key} = {value}")

    print("EXECUTED LINES:")

    previous_line = None

    for event in entry["events"]:
        if event["event"] != "line":
            continue

        if event["line"] == previous_line:
            continue

        previous_line = event["line"]
        print(f"  {event['line']}")


def main() -> int:
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    importlib.invalidate_caches()
    module = importlib.import_module(MODULE_NAME)

    detector_functions: dict[str, Callable[..., Any]] = {}
    detector_metadata = {}

    for family, function_name in DETECTORS.items():
        function = getattr(module, function_name, None)

        if function is None:
            detector_metadata[family] = {
                "name": function_name,
                "missing": True,
            }
            continue

        detector_functions[family] = function

        detector_metadata[family] = {
            "name": function_name,
            "missing": False,
            "signature": str(inspect.signature(function)),
            "source_file": inspect.getsourcefile(function),
            "source_line": inspect.getsourcelines(
                function
            )[1],
            "source": source_with_numbers(function),
        }

    sample_results = {}

    for sample_name, (
        family,
        language,
        text,
    ) in SAMPLES.items():
        function = detector_functions.get(family)

        if function is None:
            sample_results[sample_name] = {
                "family": family,
                "language": language,
                "text": text,
                "error": {
                    "type": "MissingDetector",
                    "message": DETECTORS[family],
                },
            }
            continue

        execution = execute_with_trace(
            function,
            text,
            language,
        )

        sample_results[sample_name] = {
            "family": family,
            "language": language,
            "text": text,
            **execution,
        }

    report = {
        "module": {
            "name": MODULE_NAME,
            "file": getattr(module, "__file__", None),
        },
        "detectors": detector_metadata,
        "samples": sample_results,
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

    print("\nDETECTOR SOURCES")

    for family, metadata in detector_metadata.items():
        print("\n" + "#" * 90)
        print(f"{family}: {metadata['name']}")

        if metadata.get("missing"):
            print("MISSING")
            continue

        print("SIGNATURE:", metadata["signature"])
        print(
            "LOCATION :",
            f"{metadata['source_file']}:"
            f"{metadata['source_line']}",
        )

        for item in metadata["source"]:
            print(
                f"{item['line']:>5}: "
                f"{item['text']}"
            )

    print("\n\nSAMPLE TRACE SUMMARIES")

    for sample_name, entry in sample_results.items():
        print_trace_summary(
            sample_name,
            DETECTORS[entry["family"]],
            entry,
        )

    print("\nREPORT:", REPORT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
