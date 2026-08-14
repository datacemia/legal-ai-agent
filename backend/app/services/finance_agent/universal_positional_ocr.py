from __future__ import annotations

from pathlib import Path
import re
import unicodedata

import fitz  # PyMuPDF
import pytesseract
from PIL import Image



def extract_pdf_text_preserving_layout(
    pdf_path: str | Path | None = None,
    *,
    content: bytes | None = None,
    dpi: int = 300,
    grid_width: int = 180,
    min_confidence: float = 20.0,
    psm: int = 4,
    split_merged_ocr_lines: bool = True,
    vertical_tolerance_ratio: float = 0.55,
    append_global_geometry_pass: bool = True,
    append_bidi_variants: bool = True,
    append_compact_token_variants: bool = True,
) -> str:
    """OCR a PDF while preserving horizontal and vertical page geometry.

    The PDF may be supplied either through ``pdf_path`` or directly as
    ``content`` bytes.

    OCR word x-coordinates are projected onto a fixed-width character grid.
    OCR lines are sorted by their real vertical position before rendering.

    Tesseract line groups may optionally be split into real physical rows
    using only word geometry.

    Additive compatibility pass:
    - the original grouped-line output is preserved unchanged;
    - an optional page-wide geometry reconstruction is appended;
    - optional bidirectional and compact-token variants are appended only;
    - no existing OCR line is removed or rewritten.
    """

    if pdf_path is None and not content:
        raise ValueError(
            "Either pdf_path or content must be provided"
        )

    if pdf_path is not None and content is not None:
        raise ValueError(
            "Provide pdf_path or content, not both"
        )

    if dpi < 150:
        raise ValueError(
            "dpi must be at least 150"
        )

    if grid_width < 80:
        raise ValueError(
            "grid_width must be at least 80"
        )

    if psm not in range(0, 14):
        raise ValueError(
            "psm must be between 0 and 13"
        )

    if vertical_tolerance_ratio <= 0:
        raise ValueError(
            "vertical_tolerance_ratio must be positive"
        )

    if content is not None:
        document = fitz.open(
            stream=content,
            filetype="pdf",
        )
    else:
        path = Path(pdf_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"PDF not found: {path}"
            )

        document = fitz.open(path)

    pages_out: list[str] = []

    zoom = dpi / 72.0
    matrix = fitz.Matrix(
        zoom,
        zoom,
    )

    try:
        for page_index, page in enumerate(document):
            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                (
                    pix.width,
                    pix.height,
                ),
                pix.samples,
            )

            data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT,
                config=f"--psm {psm}",
            )

            # key -> words belonging to the OCR line
            #
            # Each word stores:
            #   left, top, width, height, text
            all_words: list[
                tuple[int, int, int, int, str]
            ] = []

            grouped: dict[
                tuple[int, int, int],
                list[
                    tuple[
                        int,
                        int,
                        int,
                        int,
                        str,
                    ]
                ],
            ] = {}

            count = len(
                data.get(
                    "text",
                    [],
                )
            )

            for i in range(count):
                word = str(
                    data["text"][i] or ""
                ).strip()

                if not word:
                    continue

                try:
                    confidence = float(
                        data["conf"][i]
                    )
                except (TypeError, ValueError):
                    confidence = -1.0

                if confidence < min_confidence:
                    continue

                key = (
                    int(data["block_num"][i]),
                    int(data["par_num"][i]),
                    int(data["line_num"][i]),
                )

                left = max(
                    0,
                    int(data["left"][i]),
                )

                top = max(
                    0,
                    int(data["top"][i]),
                )

                width = max(
                    1,
                    int(data["width"][i]),
                )

                height = max(
                    1,
                    int(data["height"][i]),
                )

                item = (left, top, width, height, word)
                grouped.setdefault(key, []).append(item)
                all_words.append(item)

            # Store the real vertical coordinate with each rendered line.
            rendered_lines: list[
                tuple[int, int, str]
            ] = []

            def split_words_by_physical_row(
                words: list[
                    tuple[
                        int,
                        int,
                        int,
                        int,
                        str,
                    ]
                ],
            ) -> list[
                list[
                    tuple[
                        int,
                        int,
                        int,
                        int,
                        str,
                    ]
                ]
            ]:
                """Split one Tesseract line into real visual rows.

                This uses only page geometry:
                - no bank name;
                - no language;
                - no currency;
                - no merchant or description semantics.
                """

                if not words:
                    return []

                if not split_merged_ocr_lines:
                    return [words]

                ordered = sorted(
                    words,
                    key=lambda item: (
                        item[1],  # top
                        item[0],  # left
                    ),
                )

                ordered_heights = sorted(
                    max(
                        1,
                        item[3],
                    )
                    for item in ordered
                )

                median_height = ordered_heights[
                    len(ordered_heights) // 2
                ]

                vertical_tolerance = max(
                    2,
                    round(
                        median_height
                        * vertical_tolerance_ratio
                    ),
                )

                physical_rows: list[
                    list[
                        tuple[
                            int,
                            int,
                            int,
                            int,
                            str,
                        ]
                    ]
                ] = []

                row_centers: list[float] = []

                for word in ordered:
                    word_center = (
                        word[1]
                        + word[3] / 2.0
                    )

                    best_index: int | None = None
                    best_distance: float | None = None

                    for row_index, row_center in enumerate(
                        row_centers
                    ):
                        distance = abs(
                            word_center
                            - row_center
                        )

                        if distance > vertical_tolerance:
                            continue

                        if (
                            best_distance is None
                            or distance < best_distance
                        ):
                            best_index = row_index
                            best_distance = distance

                    if best_index is None:
                        physical_rows.append(
                            [word]
                        )

                        row_centers.append(
                            word_center
                        )

                        continue

                    physical_rows[
                        best_index
                    ].append(word)

                    row_centers[
                        best_index
                    ] = (
                        sum(
                            item[1]
                            + item[3] / 2.0
                            for item in physical_rows[
                                best_index
                            ]
                        )
                        / len(
                            physical_rows[
                                best_index
                            ]
                        )
                    )

                ordered_rows = sorted(
                    zip(
                        row_centers,
                        physical_rows,
                    ),
                    key=lambda item: item[0],
                )

                return [
                    row
                    for _center, row in ordered_rows
                ]

            split_group_count = 0
            rendered_physical_row_count = 0

            for grouped_words in grouped.values():
                if not grouped_words:
                    continue

                physical_rows = (
                    split_words_by_physical_row(
                        grouped_words
                    )
                )

                if len(physical_rows) > 1:
                    split_group_count += 1

                rendered_physical_row_count += len(
                    physical_rows
                )

                for words in physical_rows:
                    if not words:
                        continue

                    words.sort(
                        key=lambda item: (
                            item[0],  # left
                            item[1],  # top
                        )
                    )

                    line_top = min(
                        word[1]
                        for word in words
                    )

                    line_left = min(
                        word[0]
                        for word in words
                    )

                    canvas = [" "] * grid_width
                    last_end = -1

                    for (
                        left,
                        _top,
                        width,
                        _height,
                        word,
                    ) in words:
                        natural_start = round(
                            (
                                left
                                / max(
                                    1,
                                    pix.width,
                                )
                            )
                            * (
                                grid_width
                                - 1
                            )
                        )

                        start = natural_start

                        if start <= last_end:
                            start = last_end + 1

                        if start >= grid_width:
                            continue

                        visual_width = max(
                            1,
                            round(
                                (
                                    width
                                    / max(
                                        1,
                                        pix.width,
                                    )
                                )
                                * grid_width
                            ),
                        )

                        available = (
                            grid_width
                            - start
                        )

                        token = word[
                            :available
                        ]

                        for offset, char in enumerate(
                            token
                        ):
                            position = (
                                start
                                + offset
                            )

                            if position >= grid_width:
                                break

                            canvas[
                                position
                            ] = char

                        last_end = min(
                            grid_width - 1,
                            start
                            + max(
                                len(token),
                                visual_width,
                            )
                            - 1,
                        )

                    line = "".join(
                        canvas
                    ).rstrip()

                    if line.strip():
                        rendered_lines.append(
                            (
                                line_top,
                                line_left,
                                line,
                            )
                        )

            # Additive page-wide geometry pass.  This does not replace the
            # original Tesseract-group rendering above.  It reconstructs rows
            # from all accepted words on the page, which helps when Tesseract
            # assigns words from one visual table row to unrelated groups.
            augmented_lines: list[tuple[int, int, str]] = []

            def render_words_on_grid(
                words: list[tuple[int, int, int, int, str]],
            ) -> tuple[int, int, str] | None:
                if not words:
                    return None
                ordered_words = sorted(words, key=lambda item: (item[0], item[1]))
                line_top = min(item[1] for item in ordered_words)
                line_left = min(item[0] for item in ordered_words)
                canvas = [" "] * grid_width
                last_end = -1
                for left, _top, width, _height, word in ordered_words:
                    natural_start = round(
                        (left / max(1, pix.width)) * (grid_width - 1)
                    )
                    start = max(natural_start, last_end + 1)
                    if start >= grid_width:
                        continue
                    visual_width = max(
                        1, round((width / max(1, pix.width)) * grid_width)
                    )
                    token = word[: grid_width - start]
                    for offset, char in enumerate(token):
                        position = start + offset
                        if position >= grid_width:
                            break
                        canvas[position] = char
                    last_end = min(
                        grid_width - 1,
                        start + max(len(token), visual_width) - 1,
                    )
                line = "".join(canvas).rstrip()
                if not line.strip():
                    return None
                return line_top, line_left, line

            def compact_spaced_tokens(value: str) -> str:
                # Generic OCR repair for sequences such as ``1 0 . 0 0`` or
                # ``D A T E``.  It is appended as an alternative observation;
                # the original line remains available to every existing parser.
                tokens = value.split()
                output: list[str] = []
                run: list[str] = []

                def flush_run() -> None:
                    nonlocal run
                    if len(run) >= 2:
                        output.append("".join(run))
                    else:
                        output.extend(run)
                    run = []

                for token in tokens:
                    if len(token) == 1 and (token.isalnum() or token in ".,/:+-"):
                        run.append(token)
                    else:
                        flush_run()
                        output.append(token)
                flush_run()
                return " ".join(output)

            def bidi_variant(words: list[tuple[int, int, int, int, str]]) -> str | None:
                # Unicode directionality, not a language/bank/country rule.
                rtl = 0
                ltr = 0
                for *_box, text in words:
                    for char in text:
                        direction = unicodedata.bidirectional(char)
                        if direction in {"R", "AL", "AN"}:
                            rtl += 1
                        elif direction == "L":
                            ltr += 1
                if rtl <= ltr:
                    return None
                reversed_tokens = [item[4] for item in sorted(words, key=lambda x: x[0], reverse=True)]
                candidate = " ".join(reversed_tokens).strip()
                return candidate or None

            global_physical_rows: list[list[tuple[int, int, int, int, str]]] = []
            if append_global_geometry_pass and all_words:
                heights = sorted(max(1, item[3]) for item in all_words)
                median_height = heights[len(heights) // 2]
                tolerance = max(2, round(median_height * vertical_tolerance_ratio))
                centers: list[float] = []
                for word in sorted(all_words, key=lambda item: (item[1] + item[3] / 2.0, item[0])):
                    center = word[1] + word[3] / 2.0
                    best_index = None
                    best_distance = None
                    for row_index, row_center in enumerate(centers):
                        distance = abs(center - row_center)
                        if distance <= tolerance and (best_distance is None or distance < best_distance):
                            best_index = row_index
                            best_distance = distance
                    if best_index is None:
                        global_physical_rows.append([word])
                        centers.append(center)
                    else:
                        global_physical_rows[best_index].append(word)
                        centers[best_index] = sum(
                            item[1] + item[3] / 2.0
                            for item in global_physical_rows[best_index]
                        ) / len(global_physical_rows[best_index])

                for _center, row_words in sorted(zip(centers, global_physical_rows), key=lambda item: item[0]):
                    rendered = render_words_on_grid(row_words)
                    if rendered is None:
                        continue
                    augmented_lines.append(rendered)
                    top, left, line = rendered
                    if append_compact_token_variants:
                        compact_line = compact_spaced_tokens(line)
                        if compact_line and compact_line != line.strip():
                            augmented_lines.append((top, left, compact_line))
                    if append_bidi_variants:
                        bidi_line = bidi_variant(row_words)
                        if bidi_line and bidi_line != line.strip():
                            augmented_lines.append((top, left, bidi_line))
                            if append_compact_token_variants:
                                compact_bidi = compact_spaced_tokens(bidi_line)
                                if compact_bidi and compact_bidi != bidi_line:
                                    augmented_lines.append((top, left, compact_bidi))

            # Critical: restore actual top-to-bottom page order.
            rendered_lines.sort(
                key=lambda item: (
                    item[0],  # top
                    item[1],  # left
                )
            )

            print(
                "POSITIONAL_OCR_PHYSICAL_ROW_AUDIT",
                {
                    "page": page_index + 1,
                    "tesseract_groups": len(
                        grouped
                    ),
                    "groups_split": (
                        split_group_count
                    ),
                    "physical_rows": (
                        rendered_physical_row_count
                    ),
                    "rendered_lines": len(
                        rendered_lines
                    ),
                    "vertical_tolerance_ratio": (
                        vertical_tolerance_ratio
                    ),
                },
            )

            page_lines = [
                line
                for _top, _left, line
                in rendered_lines
            ]

            # Preserve original output first. Novel geometry-derived lines are
            # appended in a clearly delimited block.
            #
            # ADDITIVE v2 — geometry-anchor preservation.
            #
            # Historical behavior deduplicated augmented rows by ``line.strip()``.
            # That can remove a geometry-rendered table header merely because the
            # same visible words already exist in the base OCR stream. The
            # augmented block then contains transaction rows but no physical
            # column anchor, so downstream structural parsers cannot map cells to
            # their table columns.
            #
            # Keep the historical deduplication for ordinary rows. The only
            # additive exception is a neutral structural anchor:
            #   - no date-like token;
            #   - no digit;
            #   - at least four textual cells;
            #   - at least three preserved multi-space lanes.
            #
            # This does not inspect bank names, languages, currencies, merchants,
            # or accounting semantics. Existing page_lines are never removed or
            # rewritten.
            def _compact_geometry_key(value: str) -> str:
                return re.sub(r"\s+", " ", str(value or "")).strip()

            def _is_structural_geometry_anchor(value: str) -> bool:
                raw_line = str(value or "").rstrip()
                if not raw_line.strip():
                    return False

                if re.search(
                    r"(?<!\d)(?:\d{1,2}[./-]\d{1,2}(?:[./-]\d{2,4})?|"
                    r"\d{4}[./-]\d{1,2}[./-]\d{1,2})(?!\d)",
                    raw_line,
                ):
                    return False

                if re.search(r"\d", raw_line):
                    return False

                lanes = re.findall(r"\s{2,}", raw_line)
                if len(lanes) < 3:
                    return False

                cells = [
                    part.strip()
                    for part in re.split(r"\s{2,}", raw_line.strip())
                    if part.strip()
                ]
                if len(cells) < 4:
                    return False

                return all(
                    any(ch.isalpha() for ch in cell)
                    for cell in cells
                )

            seen_exact = {
                line.rstrip()
                for line in page_lines
                if line.strip()
            }
            seen_compact = {
                _compact_geometry_key(line)
                for line in page_lines
                if line.strip()
            }

            additive_lines: list[str] = []
            additive_exact_seen: set[str] = set()
            preserved_geometry_anchors = 0

            for _top, _left, line in sorted(
                augmented_lines, key=lambda item: (item[0], item[1], item[2])
            ):
                exact = line.rstrip()
                compact_key = _compact_geometry_key(line)

                if not compact_key:
                    continue

                is_anchor = _is_structural_geometry_anchor(line)

                # Historical path unchanged for ordinary duplicate observations.
                if compact_key in seen_compact and not is_anchor:
                    continue

                # A geometry anchor may repeat base visible text, but only one
                # augmented copy is emitted.
                if exact in additive_exact_seen:
                    continue

                if is_anchor and compact_key in seen_compact:
                    preserved_geometry_anchors += 1

                seen_exact.add(exact)
                seen_compact.add(compact_key)
                additive_exact_seen.add(exact)
                additive_lines.append(line)

            print(
                "POSITIONAL_OCR_ADDITIVE_GEOMETRY_AUDIT",
                {
                    "page": page_index + 1,
                    "source_words": len(all_words),
                    "global_rows": len(global_physical_rows),
                    "additive_lines": len(additive_lines),
                    "bidi_variants": append_bidi_variants,
                    "compact_variants": append_compact_token_variants,
                    "preserved_geometry_anchors": preserved_geometry_anchors,
                },
            )

            page_text = (
                f"[[PAGE {page_index + 1}]]\n"
                + "\n".join(page_lines)
            )
            if additive_lines:
                page_text += (
                    "\n[[OCR_GEOMETRY_AUGMENTED_PAGE "
                    f"{page_index + 1}]]\n"
                    + "\n".join(additive_lines)
                )

            # ADDITIVE v3: preserve the exact fixed-grid geometry in an opaque
            # letters-only sidecar.  Some downstream text-normalization layers
            # collapse whitespace before family parsers run.  The sidecar is
            # deliberately non-transactional to every legacy parser: it contains
            # no digits, dates or monetary tokens until explicitly decoded by a
            # geometry-aware family parser.
            #
            # Encoding: each UTF-8 byte becomes two letters A..P (high/low nibble).
            # This is reversible and survives whitespace compaction unchanged.
            exact_geometry_lines: list[str] = []

            def _encode_geometry_line(value: str) -> str:
                raw_bytes = value.encode("utf-8")
                alphabet = "ABCDEFGHIJKLMNOP"
                return "".join(
                    alphabet[(byte >> 4) & 0x0F]
                    + alphabet[byte & 0x0F]
                    for byte in raw_bytes
                )

            for row_words in global_physical_rows:
                rendered = render_words_on_grid(row_words)
                if rendered is None:
                    continue
                _top, _left, exact_line = rendered
                if exact_line.strip():
                    exact_geometry_lines.append(
                        _encode_geometry_line(exact_line)
                    )

            if exact_geometry_lines:
                page_text += (
                    "\n[[OCR_GEOMETRY_EXACT_PAGE "
                    f"{page_index + 1}]]\n"
                    + "\n".join(exact_geometry_lines)
                )

            print(
                "POSITIONAL_OCR_EXACT_GEOMETRY_SIDECAR_AUDIT",
                {
                    "page": page_index + 1,
                    "exact_geometry_rows": len(exact_geometry_lines),
                    "encoding": "letters_only_nibbles",
                },
            )

            pages_out.append(page_text)

    finally:
        document.close()

    result = "\n\n".join(
        pages_out
    ).strip()

    if not result:
        return ""

    return result + "\n"

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "OCR a PDF while preserving horizontal "
            "and vertical table geometry."
        )
    )

    parser.add_argument("pdf")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--grid-width", type=int, default=180)
    parser.add_argument("--min-confidence", type=float, default=20.0)
    parser.add_argument("--psm", type=int, default=4)

    args = parser.parse_args()

    result = extract_pdf_text_preserving_layout(
        pdf_path=args.pdf,
        dpi=args.dpi,
        grid_width=args.grid_width,
        min_confidence=args.min_confidence,
        psm=args.psm,
    )

    Path(args.output).write_text(
        result,
        encoding="utf-8",
    )