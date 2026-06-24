$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Error "winget is not available. Please install it from https://aka.ms/getwinget"
    exit 1
}

$tesseractDefault = "C:\Program Files\Tesseract-OCR"
$tesseractInPath = $env:PATH -split ";" | Where-Object { Test-Path "$_\tesseract.exe" }

if (-not $tesseractInPath) {
    Write-Host "Installing Tesseract via winget..."
    winget install --id UB-Mannheim.TesseractOCR --silent --accept-package-agreements --accept-source-agreements

    if (Test-Path $tesseractDefault) {
        $currentPath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
        if ($currentPath -notlike "*Tesseract-OCR*") {
            [System.Environment]::SetEnvironmentVariable("PATH", "$currentPath;$tesseractDefault", "Machine")
            $env:PATH = "$env:PATH;$tesseractDefault"
            Write-Host "Tesseract added to PATH."
        }
    }
} else {
    Write-Host "Tesseract already in PATH, skipping install."
}

Write-Host "Installing Python dependencies..."
pip install -r "$ScriptDir\requirements.txt"

if ($ScriptDir -match '[&|<>]') {
    Write-Error "Installation path contains characters unsafe for batch files: $ScriptDir"
    exit 1
}

$batPath = "$ScriptDir\convert-to-md.bat"
$batContent = "@echo off`r`npython `"$ScriptDir\convert.py`" %*"
Set-Content -Path $batPath -Value $batContent -Encoding ASCII

Write-Host ""
Write-Host "Installation complete."
Write-Host "Usage: convert-to-md file1.pdf file2.docx file3.xlsx"
Write-Host "Note: Add '$ScriptDir' to your PATH to use 'convert-to-md' from anywhere."
