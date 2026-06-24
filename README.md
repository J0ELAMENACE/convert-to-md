# convert-to-md

Convert documents to Markdown from the command line.

## Supported Formats

| Extension       | Library         | Notes                              |
|-----------------|-----------------|------------------------------------|
| `.pdf`          | pdfplumber      | Text extraction                    |
| `.docx`         | mammoth         | Word documents                     |
| `.pptx`         | python-pptx     | One section per slide              |
| `.xlsx`         | openpyxl        | Each sheet as a Markdown table     |
| `.csv`          | stdlib csv      | Markdown table                     |
| `.html` / `.htm`| beautifulsoup4  | Plain text extraction              |
| `.txt`          | —               | Passed through as-is               |
| `.rst`          | —               | Code blocks wrapped in fences      |
| `.org`          | —               | Passed through as-is               |
| `.ipynb`        | —               | Markdown cells as-is, code fenced  |
| `.png` / `.jpg` / `.jpeg` | pytesseract + Pillow | OCR          |

Unsupported files print `Unsupported: <filename>` and are skipped.

## Installation

### Linux

```bash
chmod +x install.sh
./install.sh
```

The script detects your package manager (`apt`, `dnf`, `pacman`, or `zypper`), installs `python3`, `pip`, and `tesseract-ocr`, installs Python dependencies, and copies `convert-to-md` to `/usr/local/bin`.

### Windows

Open PowerShell as Administrator and run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

The script installs Tesseract via `winget`, adds it to `PATH`, installs Python dependencies, and creates a `convert-to-md.bat` wrapper in the project directory.

Add the project directory to your `PATH` to use `convert-to-md` from anywhere.

## Usage

```bash
convert-to-md file1.pdf file2.docx file3.xlsx
```

Output `.md` files are written to `md-converter/converted/`. The original extension is included in the output filename to prevent collisions between files that share the same stem (e.g. `report.pdf` and `report.docx`).

```
converted/
├── file1_pdf.md
├── file2_docx.md
└── file3_xlsx.md
```

### Examples

```bash
# Single file
convert-to-md report.pdf

# Multiple files
convert-to-md slides.pptx data.xlsx notes.txt

# Mixed formats including OCR
convert-to-md scan.png document.docx notebook.ipynb
```

## Requirements

- Python 3.8+
- Tesseract OCR (installed by the install scripts)
