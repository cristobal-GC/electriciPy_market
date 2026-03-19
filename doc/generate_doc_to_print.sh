#!/bin/bash

set -e

# Directories
RULES_DIR="rules"
WIND_DIR="wind_forecasts"

# Files
GENERAL="$RULES_DIR/general_rules.pdf"
WIND="$WIND_DIR/wind_forecasts.pdf"

# Check that the main files exist
if [ ! -f "$GENERAL" ]; then
    echo "Error: $GENERAL not found."
    exit 1
fi

if [ ! -f "$WIND" ]; then
    echo "Error: $WIND not found."
    exit 1
fi

# List of particular PDFs, sorted alphabetically
particular_files=($(ls "$RULES_DIR"/particular_*.pdf 2>/dev/null | sort))
if [ ${#particular_files[@]} -eq 0 ]; then
    echo "No particular PDFs found in $RULES_DIR."
    exit 1
fi

# Temporary directory
TMPDIR=$(mktemp -d)

# Generate the interleaved list: general + particular
LIST_FILES=()
for f in "${particular_files[@]}"; do
    LIST_FILES+=("$GENERAL")
    LIST_FILES+=("$f")
done

# Temporary intermediate PDF
INTERMEDIATE="$TMPDIR/intermediate.pdf"

# Combine general + particular PDFs
pdfunite "${LIST_FILES[@]}" "$INTERMEDIATE"

# --- Now process wind_forecasts.pdf ---
# Extract page 1 and page 2
pdftk "$WIND" cat 1 output "$TMPDIR/wind_page1.pdf"
pdftk "$WIND" cat 2 output "$TMPDIR/wind_page2.pdf"

# Create a blank page
# Using ps2pdf (if not installed: sudo apt install ghostscript)
echo " " | ps2pdf - "$TMPDIR/blank.pdf"

# Combine wind_forecasts: page1 + blank + page2
pdfunite "$TMPDIR/wind_page1.pdf" "$TMPDIR/blank.pdf" "$TMPDIR/wind_page2.pdf" "$TMPDIR/wind_final.pdf"

# --- Combine everything ---
OUTPUT="doc_to_print.pdf"
pdfunite "$INTERMEDIATE" "$TMPDIR/wind_final.pdf" "$OUTPUT"

# Clean up temporary files
rm -r "$TMPDIR"

echo "Combined PDF created: $OUTPUT"