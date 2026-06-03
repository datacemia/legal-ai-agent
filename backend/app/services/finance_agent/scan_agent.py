import fitz
import pytesseract
from PIL import Image
import io


def scan_agent_extract_text(
    file_path: str | None = None,
    content: bytes | None = None,
) -> str:
    text_parts = []

    try:
        if content:
            doc = fitz.open(stream=content, filetype="pdf")
        elif file_path:
            doc = fitz.open(file_path)
        else:
            return ""

        with doc:
            for page in doc:
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2),
                    alpha=False,
                )

                image = Image.open(
                    io.BytesIO(pix.tobytes("png"))
                )

                page_text = pytesseract.image_to_string(
                    image,
                    lang="eng+fra+ara",
                )

                if page_text:
                    text_parts.append(page_text)

    except Exception as e:
        print("SCAN_AGENT_EXTRACT_FAILED", str(e))
        return ""

    return "\n".join(text_parts).strip()
