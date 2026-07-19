#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


TARGET = Path("scripts/trace_semantic_pipeline.py")

ANCHOR = "from pathlib import Path\n"

INSERTION = '''
from pathlib import Path

# Make the backend repository root importable when this script is
# launched through: python scripts/trace_semantic_pipeline.py
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
'''


def main() -> int:
    if not TARGET.exists():
        print(f"ERROR: missing file: {TARGET}")
        return 1

    content = TARGET.read_text(encoding="utf-8")

    marker = (
        "REPOSITORY_ROOT = "
        "Path(__file__).resolve().parents[1]"
    )

    if marker in content:
        print("PATH FIX ALREADY PRESENT")
        print("TARGET:", TARGET)
        return 0

    if ANCHOR not in content:
        print("ERROR: pathlib import not found")
        return 2

    content = content.replace(
        ANCHOR,
        INSERTION,
        1,
    )

    TARGET.write_text(
        content,
        encoding="utf-8",
    )

    print("=" * 72)
    print("TRACE SCRIPT PATH FIX APPLIED")
    print("=" * 72)
    print("TARGET:", TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
