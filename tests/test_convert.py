import json
import pathlib
import tempfile
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from convert import _rows_to_md_table, convert_txt, convert_csv, convert_rst, convert_org, convert_ipynb, convert_html


# ── _rows_to_md_table ────────────────────────────────────────────────────────

def test_rows_to_md_table_empty():
    assert _rows_to_md_table([]) == ""


def test_rows_to_md_table_header_only():
    result = _rows_to_md_table([["Name", "Age"]])
    assert "Name" in result
    assert "Age" in result
    assert "---" in result


def test_rows_to_md_table_with_data():
    rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    result = _rows_to_md_table(rows)
    assert "Alice" in result
    assert "Bob" in result
    assert "|" in result


def test_rows_to_md_table_column_alignment():
    rows = [["A", "B"], ["short", "x"]]
    result = _rows_to_md_table(rows)
    lines = result.splitlines()
    assert len(lines) == 3  # header, separator, data row


# ── convert_txt ──────────────────────────────────────────────────────────────

def test_convert_txt_basic():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("Hello world")
        tmp = pathlib.Path(f.name)
    assert convert_txt(tmp) == "Hello world"
    tmp.unlink()


def test_convert_txt_multiline():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("line1\nline2\nline3")
        tmp = pathlib.Path(f.name)
    result = convert_txt(tmp)
    assert "line1" in result
    assert "line3" in result
    tmp.unlink()


def test_convert_txt_empty():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("")
        tmp = pathlib.Path(f.name)
    assert convert_txt(tmp) == ""
    tmp.unlink()


# ── convert_csv ──────────────────────────────────────────────────────────────

def test_convert_csv_basic():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("Name,Age\nAlice,30\nBob,25")
        tmp = pathlib.Path(f.name)
    result = convert_csv(tmp)
    assert "Alice" in result
    assert "Name" in result
    assert "|" in result
    tmp.unlink()


def test_convert_csv_single_column():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("Item\nA\nB")
        tmp = pathlib.Path(f.name)
    result = convert_csv(tmp)
    assert "Item" in result
    tmp.unlink()


# ── convert_rst ──────────────────────────────────────────────────────────────

def test_convert_rst_passthrough():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".rst", delete=False, encoding="utf-8") as f:
        f.write("Title\n=====\n\nSome text here.")
        tmp = pathlib.Path(f.name)
    result = convert_rst(tmp)
    assert "Title" in result
    assert "Some text here." in result
    tmp.unlink()


def test_convert_rst_code_block():
    content = ".. code::\n\n   print('hello')\n\nAfter."
    with tempfile.NamedTemporaryFile(mode="w", suffix=".rst", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = pathlib.Path(f.name)
    result = convert_rst(tmp)
    assert "```" in result
    assert "print('hello')" in result
    tmp.unlink()


# ── convert_org ──────────────────────────────────────────────────────────────

def test_convert_org_returns_content():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".org", delete=False, encoding="utf-8") as f:
        f.write("* Heading\n\nSome content.")
        tmp = pathlib.Path(f.name)
    result = convert_org(tmp)
    assert "Heading" in result
    assert "Some content." in result
    tmp.unlink()


# ── convert_ipynb ─────────────────────────────────────────────────────────────

def test_convert_ipynb_markdown_and_code():
    nb = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title\n", "Some text."]},
            {"cell_type": "code", "source": ["print('hello')"]},
        ]
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False, encoding="utf-8") as f:
        json.dump(nb, f)
        tmp = pathlib.Path(f.name)
    result = convert_ipynb(tmp)
    assert "# Title" in result
    assert "```python" in result
    assert "print('hello')" in result
    tmp.unlink()


def test_convert_ipynb_invalid_raises():
    bad = {"not_a_notebook": True}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False, encoding="utf-8") as f:
        json.dump(bad, f)
        tmp = pathlib.Path(f.name)
    with pytest.raises(ValueError, match="missing 'cells' key"):
        convert_ipynb(tmp)
    tmp.unlink()


def test_convert_ipynb_empty_notebook():
    nb = {"cells": []}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False, encoding="utf-8") as f:
        json.dump(nb, f)
        tmp = pathlib.Path(f.name)
    result = convert_ipynb(tmp)
    assert result == ""
    tmp.unlink()


# ── convert_html ─────────────────────────────────────────────────────────────

def test_convert_html_extracts_text():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write("<html><body><h1>Hello</h1><p>World</p></body></html>")
        tmp = pathlib.Path(f.name)
    result = convert_html(tmp)
    assert "Hello" in result
    assert "World" in result
    tmp.unlink()


def test_convert_html_strips_tags():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write("<b>Bold</b><i>Italic</i>")
        tmp = pathlib.Path(f.name)
    result = convert_html(tmp)
    assert "<b>" not in result
    assert "Bold" in result
    tmp.unlink()
