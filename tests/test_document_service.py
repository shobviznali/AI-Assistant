from app.services.document_service import read_document, process_document
from pathlib import Path
import pytest

def test_read_md(tmp_path):
    file = tmp_path / "test.md"
    file.write_text("Hello AI", encoding="utf-8")

    result = read_document(str(file))

    assert result == "Hello AI"


def test_read_txt(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello AI", encoding="utf-8")

    result = read_document(str(file))

    assert result == "Hello AI"


def test_invalid_extension(tmp_path):
    file = tmp_path / "test.pdf"
    file.write_text("Hello AI", encoding="utf-8")

    with pytest.raises(ValueError):
        read_document(str(file))


def test_uppercase_extension(tmp_path):
    file = tmp_path / "test.MD"
    file.write_text("Hello AI", encoding="utf-8")

    result = read_document(str(file))

    assert result == "Hello AI"


def test_file_not_found(tmp_path):
    file = tmp_path / "nonexistent.md"

    with pytest.raises(ValueError):
        read_document(str(file))


def test_process_document(tmp_path):
    file = tmp_path / "test.md"
    file.write_text("A" * 900, encoding='utf-8')
    result = process_document(str(file),"doc123", "hr")

    assert len(result) == 2
    assert result[0]["document_id"] == "doc123"
    assert result[0]["filename"] == "test.md"
    assert result[0]["owner_group"] == "hr"
    assert len(result[0]["text"]) == 500