import PyPDF2
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file."""
    try:
        pdf_bytes = uploaded_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            raise ValueError(
                "No text found in PDF. It may be a scanned image-based PDF. "
                "Please try a text-based PDF or paste content as a TXT file."
            )
        return text.strip()
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")


def extract_text_from_txt(uploaded_file) -> str:
    """Extract text from an uploaded TXT file."""
    try:
        return uploaded_file.read().decode("utf-8").strip()
    except Exception as e:
        raise ValueError(f"Failed to read text file: {str(e)}")


def extract_text(uploaded_file) -> str:
    """Route to the correct extractor based on file type."""
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or TXT file."
        )