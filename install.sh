#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_system_deps() {
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -q
        sudo apt-get install -y python3 python3-pip tesseract-ocr
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip tesseract
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm python python-pip tesseract
    elif command -v zypper &>/dev/null; then
        sudo zypper install -y python3 python3-pip tesseract-ocr
    else
        echo "No supported package manager found (apt, dnf, pacman, zypper)." >&2
        exit 1
    fi
}

install_system_deps

pip3 install -r "$SCRIPT_DIR/requirements.txt"

sudo cp "$SCRIPT_DIR/convert.py" /usr/local/bin/convert-to-md
sudo chmod +x /usr/local/bin/convert-to-md

echo ""
echo "Installation complete."
echo "Usage: convert-to-md file1.pdf file2.docx file3.xlsx"
