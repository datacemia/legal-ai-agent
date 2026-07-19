from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


path = (
    Path.cwd()
    / "app"
    / "services"
    / "contract_agent"
    / "normalized_legal_relation.py"
).resolve()

if not path.is_file():
    raise SystemExit(f"ABORT: fichier introuvable : {path}")

source = path.read_text(encoding="utf-8")

marker = "[NORMALIZED_RELATION_TRACE]"

anchor = '''    item["normalized_concept"] = normalized_concept
    item["normalized_relation"] = relation
    item["normalized_polarity"] = normalized_polarity
'''

replacement = '''    # Temporary normalized-relation diagnostic.
    # Disabled unless LEGAL_AI_TRACE_NORMALIZED_RELATION=1.
    if os.environ.get(
        "LEGAL_AI_TRACE_NORMALIZED_RELATION"
    ) == "1":
        traced_concepts = {
            "PARTICIPATION_OPTION",
            "PREEMPTIVE_RIGHT",
            "INVESTOR_CONSENT_RIGHT",
        }

        if normalized_concept in traced_concepts:
            print(
                "[NORMALIZED_RELATION_TRACE]",
                json.dumps(
                    {
                        "raw_kind": item.get("kind"),
                        "normalized_concept": normalized_concept,
                        "roles": roles,
                        "explicit_right_holder": (
                            explicit_right_holder
                        ),
                        "right_holder": right_holder,
                        "obligated_actor": obligated_actor,
                        "counterparty": counterparty,
                        "beneficiary": beneficiary,
                        "normalized_object": normalized_object,
                        "action": relation.get("action"),
                        "polarity": relation.get("polarity"),
                        "normalized_relation": relation,
                        "local_text": local_text,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                flush=True,
            )

    item["normalized_concept"] = normalized_concept
    item["normalized_relation"] = relation
    item["normalized_polarity"] = normalized_polarity
'''


def ensure_import(text: str, module: str) -> str:
    tree = ast.parse(text)

    for node in tree.body:
        if isinstance(node, ast.Import):
            if any(alias.name == module for alias in node.names):
                return text

    lines = text.splitlines(keepends=True)
    insert_at = 0

    if lines and lines[0].startswith("#!"):
        insert_at = 1

    while (
        insert_at < len(lines)
        and (
            "coding:" in lines[insert_at]
            or "coding=" in lines[insert_at]
        )
    ):
        insert_at += 1

    while (
        insert_at < len(lines)
        and lines[insert_at].startswith(
            "from __future__ import"
        )
    ):
        insert_at += 1

    lines.insert(insert_at, f"import {module}\n")
    return "".join(lines)


print("TARGET:", path)

if marker in source:
    print("Trace déjà présente.")
    raise SystemExit(0)

anchor_count = source.count(anchor)

if anchor_count != 1:
    raise SystemExit(
        f"ABORT: ancre trouvée {anchor_count} fois. "
        "Aucun fichier modifié."
    )

patched = source.replace(anchor, replacement, 1)
patched = ensure_import(patched, "json")
patched = ensure_import(patched, "os")

ast.parse(patched)
compile(patched, str(path), "exec")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = path.with_name(
    f"{path.name}.bak_trace_{timestamp}"
)

shutil.copy2(path, backup)
path.write_text(patched, encoding="utf-8")

persisted = path.read_text(encoding="utf-8")

if marker not in persisted:
    shutil.copy2(backup, path)
    raise SystemExit(
        "ABORT: marqueur absent après écriture. "
        "Sauvegarde restaurée."
    )

ast.parse(persisted)
compile(persisted, str(path), "exec")

print("PATCHED:", path)
print("BACKUP :", backup)
print("TRACE  : installed")
