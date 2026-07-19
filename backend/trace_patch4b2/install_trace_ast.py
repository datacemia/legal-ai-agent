from __future__ import annotations

import ast
import shutil
import textwrap
from datetime import datetime
from pathlib import Path


PATH = Path(
    "app/services/contract_agent/"
    "normalized_legal_relation.py"
).resolve()

MARKER = "[NORMALIZED_RELATION_TRACE]"

TRACE_SOURCE = textwrap.dedent(
    '''
    # Temporary normalized-relation diagnostic.
    # Disabled unless LEGAL_AI_TRACE_NORMALIZED_RELATION=1.
    if __import__("os").environ.get(
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
                __import__("json").dumps(
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
    '''
).lstrip()


def find_materializer(
    tree: ast.Module,
) -> ast.FunctionDef | ast.AsyncFunctionDef:
    matches = [
        node
        for node in tree.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
        and node.name == "materialize_normalized_relation"
    ]

    if len(matches) != 1:
        raise SystemExit(
            "ABORT: materialize_normalized_relation "
            f"trouvé {len(matches)} fois."
        )

    return matches[0]


def find_return_item(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> ast.Return:
    matches = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Return)
        and isinstance(node.value, ast.Name)
        and node.value.id == "item"
    ]

    if len(matches) != 1:
        raise SystemExit(
            "ABORT: return item trouvé "
            f"{len(matches)} fois."
        )

    return matches[0]


def indent_block(
    block: str,
    spaces: int,
) -> str:
    prefix = " " * spaces

    return "".join(
        prefix + line if line.strip() else line
        for line in block.splitlines(keepends=True)
    )


def main() -> None:
    if not PATH.is_file():
        raise SystemExit(
            f"ABORT: fichier introuvable : {PATH}"
        )

    source = PATH.read_text(encoding="utf-8")

    print("TARGET:", PATH)

    # Confirm that the current source is valid before patching.
    ast.parse(source)
    compile(source, str(PATH), "exec")

    if MARKER in source:
        print("Trace déjà présente.")
        return

    tree = ast.parse(source)
    function = find_materializer(tree)
    return_node = find_return_item(function)

    lines = source.splitlines(keepends=True)
    insertion_index = return_node.lineno - 1

    trace_block = indent_block(
        TRACE_SOURCE,
        return_node.col_offset,
    )

    # Ensure the inserted block ends before `return item`.
    if not trace_block.endswith("\n"):
        trace_block += "\n"

    lines.insert(insertion_index, trace_block)
    patched = "".join(lines)

    # Validate before touching the source file.
    try:
        ast.parse(patched)
        compile(patched, str(PATH), "exec")
    except SyntaxError as exc:
        print(
            "FAILED PATCH LINE:",
            exc.lineno,
            exc.msg,
        )

        preview = patched.splitlines()
        start = max(0, (exc.lineno or 1) - 8)
        end = min(len(preview), (exc.lineno or 1) + 7)

        for index in range(start, end):
            print(
                f"{index + 1:5}: "
                f"{preview[index]!r}"
            )

        raise SystemExit(
            "ABORT: source patchée invalide; "
            "fichier original inchangé."
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    backup = PATH.with_name(
        f"{PATH.name}.bak_trace_{timestamp}"
    )

    shutil.copy2(PATH, backup)

    try:
        PATH.write_text(
            patched,
            encoding="utf-8",
        )

        persisted = PATH.read_text(
            encoding="utf-8",
        )

        ast.parse(persisted)
        compile(
            persisted,
            str(PATH),
            "exec",
        )

        if MARKER not in persisted:
            raise RuntimeError(
                "Marqueur absent après écriture."
            )

    except Exception:
        shutil.copy2(backup, PATH)
        raise

    print("PATCHED:", PATH)
    print("BACKUP :", backup)
    print(
        "RETURN LINE:",
        return_node.lineno,
    )
    print(
        "INDENTATION:",
        return_node.col_offset,
    )


if __name__ == "__main__":
    main()
