#!/bin/bash

set -e

# Directorios
RULES_DIR="rules"
WIND_DIR="wind_forecasts"

# Archivos
GENERAL="$RULES_DIR/general_rules.pdf"
WIND="$WIND_DIR/wind_forecasts.pdf"

# Comprobar que existan los archivos principales
if [ ! -f "$GENERAL" ]; then
    echo "Error: $GENERAL no encontrado."
    exit 1
fi

if [ ! -f "$WIND" ]; then
    echo "Error: $WIND no encontrado."
    exit 1
fi

# Lista de particulares ordenada
particular_files=($(ls "$RULES_DIR"/particular_*.pdf 2>/dev/null | sort))
if [ ${#particular_files[@]} -eq 0 ]; then
    echo "No se encontraron archivos particulares en $RULES_DIR."
    exit 1
fi

# Directorio temporal
TMPDIR=$(mktemp -d)

# Generar lista de PDFs intercalados: general + particular
LIST_FILES=()
for f in "${particular_files[@]}"; do
    LIST_FILES+=("$GENERAL")
    LIST_FILES+=("$f")
done

# Archivo temporal intermedio
INTERMEDIATE="$TMPDIR/intermediate.pdf"

# Unir general + particulares
pdfunite "${LIST_FILES[@]}" "$INTERMEDIATE"

# --- Ahora procesar wind_forecasts.pdf ---
# Extraer página 1 y 2
pdftk "$WIND" cat 1 output "$TMPDIR/wind_page1.pdf"
pdftk "$WIND" cat 2 output "$TMPDIR/wind_page2.pdf"

# Crear una página en blanco
# Usamos pdfjam (si no está, instalar: sudo apt install texlive-extra-utils)
echo " " | ps2pdf - "$TMPDIR/blank.pdf"

# Combinar wind_forecasts: page1 + blank + page2
pdfunite "$TMPDIR/wind_page1.pdf" "$TMPDIR/blank.pdf" "$TMPDIR/wind_page2.pdf" "$TMPDIR/wind_final.pdf"

# --- Combinar todo ---
OUTPUT="doc_to_print.pdf"
pdfunite "$INTERMEDIATE" "$TMPDIR/wind_final.pdf" "$OUTPUT"

# Limpiar
rm -r "$TMPDIR"

echo "PDF combinado creado: $OUTPUT"