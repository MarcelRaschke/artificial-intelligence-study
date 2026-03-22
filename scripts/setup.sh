#!/usr/bin/env bash
set -euo pipefail

# Unified Setup Script for artificial-intelligence-study
# Installs all Python dependencies needed across the repository.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# --- Check prerequisites ---

if ! command -v python3 &>/dev/null; then
    error "Python 3 is required but not found. Install it from https://www.python.org/"
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
info "Found Python $PYTHON_VERSION"

if ! command -v pip3 &>/dev/null && ! python3 -m pip --version &>/dev/null 2>&1; then
    error "pip is required but not found. Install it with: python3 -m ensurepip"
fi

# --- Create virtual environment ---

VENV_DIR="$PROJECT_DIR/venv"

if [ -d "$VENV_DIR" ]; then
    info "Virtual environment already exists at $VENV_DIR"
else
    info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    info "Virtual environment created at $VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"
info "Virtual environment activated"

# Upgrade pip
pip install --upgrade pip --quiet

# --- Install dependencies ---

info "Installing core packages (numpy, pandas, matplotlib, scikit-learn)..."
pip install --quiet numpy pandas matplotlib scikit-learn

info "Installing deep learning frameworks (tensorflow, keras, torch)..."
pip install --quiet tensorflow keras torch

info "Installing NLP packages (nltk, gensim)..."
pip install --quiet nltk gensim

info "Installing image processing packages (Pillow, pytesseract)..."
pip install --quiet Pillow pytesseract

info "Installing web/serving packages (flask)..."
pip install --quiet flask

info "Installing Jupyter..."
pip install --quiet jupyter notebook

# --- Summary ---

echo ""
info "Setup complete!"
echo ""
info "To activate the virtual environment:"
info "  source $VENV_DIR/bin/activate"
echo ""
info "Installed packages:"
pip list --format=columns 2>/dev/null | head -30 || true
echo "  ..."
echo ""
info "To run Jupyter notebooks:"
info "  jupyter notebook"
echo ""
