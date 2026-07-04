#!/bin/zsh
set -euo pipefail

ENGINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$ENGINE_DIR/source"
OUTPUT_DIR="${RESUME_OUTPUT_DIR:-$ENGINE_DIR/../resumes}"
BUILD_DIR="${RESUME_BUILD_DIR:-$ENGINE_DIR/output/build}"

COMPANY="Company"
ROLE="Role"
ENGINE="xelatex"
REQUIRE_ONE_PAGE=0

usage() {
  cat <<'EOF'
Usage:
  ./scripts/build_resume.sh --company "Company" --role "Role"

Options:
  --company NAME        Company name for output filename
  --role ROLE          Role name for output filename
  --engine ENGINE      xelatex or pdflatex (default: xelatex)
  --output-dir DIR     Directory for the final PDF
  --build-dir DIR      Directory for temporary LaTeX build files
  --require-one-page   Exit non-zero when the compiled PDF is not exactly one page
  -h, --help           Show this help
EOF
}

sanitize_name() {
  local value="$1"
  printf "%s" "$value" | iconv -c -t ASCII//TRANSLIT 2>/dev/null | sed -E 's/&/and/g; s/[^A-Za-z0-9]+/_/g; s/^_+//; s/_+$//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --company)
      COMPANY="$2"
      shift 2
      ;;
    --role)
      ROLE="$2"
      shift 2
      ;;
    --engine)
      ENGINE="$2"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --build-dir)
      BUILD_DIR="$2"
      shift 2
      ;;
    --require-one-page)
      REQUIRE_ONE_PAGE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -f "$SOURCE_DIR/main.tex" ]]; then
  echo "Missing LaTeX entrypoint: $SOURCE_DIR/main.tex" >&2
  exit 2
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "Missing latexmk. Install a TeX distribution such as MacTeX or TeX Live." >&2
  exit 2
fi

case "$ENGINE" in
  xelatex)
    LATEXMK_ENGINE="-xelatex"
    ;;
  pdflatex)
    LATEXMK_ENGINE="-pdf"
    ;;
  *)
    echo "Unsupported engine: $ENGINE. Use xelatex or pdflatex." >&2
    exit 2
    ;;
esac

COMPANY_SLUG="$(sanitize_name "$COMPANY")"
ROLE_SLUG="$(sanitize_name "$ROLE")"
JOB_NAME="${COMPANY_SLUG:-Company}_${ROLE_SLUG:-Role}_Resume"

mkdir -p "$OUTPUT_DIR" "$BUILD_DIR"

pushd "$SOURCE_DIR" >/dev/null
latexmk "$LATEXMK_ENGINE" -interaction=nonstopmode -halt-on-error -outdir="$BUILD_DIR" -jobname="$JOB_NAME" main.tex
popd >/dev/null

BUILD_PDF_PATH="$BUILD_DIR/$JOB_NAME.pdf"
FINAL_PDF_PATH="$OUTPUT_DIR/$JOB_NAME.pdf"
LOG_PATH="$BUILD_DIR/$JOB_NAME.log"

if [[ ! -f "$BUILD_PDF_PATH" ]]; then
  echo "Build finished but PDF was not found: $BUILD_PDF_PATH" >&2
  exit 1
fi

cp "$BUILD_PDF_PATH" "$FINAL_PDF_PATH"

PAGES="unknown"
if command -v pdfinfo >/dev/null 2>&1; then
  PAGES="$(pdfinfo "$FINAL_PDF_PATH" | awk '/^Pages:/ {print $2}')"
fi

WARNINGS="unknown"
if [[ -f "$LOG_PATH" ]]; then
  WARNINGS="$( { grep -E "Warning|Overfull|Underfull|Missing character|Font shape" "$LOG_PATH" || true; } | wc -l | tr -d ' ')"
fi

echo "PDF: $FINAL_PDF_PATH"
echo "Engine: $ENGINE"
echo "Pages: $PAGES"
echo "Warnings/overflow lines: $WARNINGS"

if [[ "$REQUIRE_ONE_PAGE" == "1" && "$PAGES" != "1" ]]; then
  echo "PDF is not strictly one page." >&2
  exit 3
fi
