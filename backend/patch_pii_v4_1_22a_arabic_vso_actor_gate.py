import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/pii_redactor.py"
)

OLD = '''    if actor_predicate_after:
        return True

    return False
'''

NEW = '''    if actor_predicate_after:
        return True

    # Arabic commonly uses verb-subject-object order. A real contractual
    # organization may therefore follow its operative predicate rather than
    # precede it. Keep this backward signal intentionally narrow: only
    # substantive contractual actor verbs immediately before the GLiNER span
    # qualify. This is syntax-based, not domain-, family-, or entity-specific.
    arabic_actor_predicate_before = re.search(
        r"(?:"
        r"يلتزم|تلتزم|"
        r"يقدم|تقدم|"
        r"يوفر|توفر|"
        r"ينفذ|تنفذ|"
        r"يدفع|تدفع|"
        r"يسدد|تسدد|"
        r"يعوض|تعوض|"
        r"يخطر|تخطر|"
        r"يبلغ|تبلغ|"
        r"يحافظ|تحافظ|"
        r"يتعهد|تتعهد|"
        r"يمنح|تمنح|"
        r"يعين|تعين|"
        r"يتحمل|تتحمل"
        r")\\s+$",
        before,
        re.IGNORECASE,
    )

    if arabic_actor_predicate_before:
        return True

    return False
'''


def main():
    source = TARGET.read_text(
        encoding="utf-8"
    )

    ast.parse(source)

    if source.count(OLD) != 1:
        raise SystemExit(
            "ABORT: expected exactly one actor-gate tail"
        )

    if "arabic_actor_predicate_before" in source:
        raise SystemExit(
            "ABORT: V4.1.22A already installed"
        )

    stamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = TARGET.with_name(
        TARGET.name
        + ".before_v4_1_22a_"
        + stamp
    )

    shutil.copy2(
        TARGET,
        backup,
    )

    updated = source.replace(
        OLD,
        NEW,
        1,
    )

    ast.parse(updated)
    compile(
        updated,
        str(TARGET),
        "exec",
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 96)
    print("V4.1.22A ARABIC VSO ACTOR GATE APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print(
        "A: EN/FR forward actor evidence unchanged"
    )
    print(
        "B: Arabic narrow verb-before-organization actor evidence added"
    )
    print(
        "C: framework/domain preservation gate unchanged"
    )
    print(
        "D: person privacy behavior unchanged"
    )
    print(
        "E: GLiNER threshold and chunking unchanged"
    )
    print(
        "UNTOUCHED: semantic profile, family detector, publication gate,"
    )
    print(
        "           risk scoring, taxonomy, summary, frontend"
    )
    print("AST: OK")
    print("=" * 96)


if __name__ == "__main__":
    main()
