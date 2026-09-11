#!/usr/bin/env bash
set -euo pipefail

# AI Study Repository Setup Script
# Creates Python virtual environment and installs ML dependencies

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# --- Check prerequisites ---

check_python() {
    if command -v python3 &>/dev/null; then
        local version
        version=$(python3 --version 2>&1 | awk '{print $2}')
        local major
        major=$(echo "$version" | cut -d. -f1)
        if [ "$major" -ge 3 ]; then
            info "Python $version found"
            return 0
        else
            error "Python 3 required, found $version"
            return 1
        fi
    else
        error "Python 3 not found"
        return 1
    fi
}

check_pip() {
    if command -v pip3 &>/dev/null; then
        info "pip3 found"
        return 0
    else
        error "pip3 not found"
        return 1
    fi
}

# --- Setup venv ---

setup_venv() {
    if [ -d "$PROJECT_DIR/venv" ]; then
        info "Virtual environment already exists at $PROJECT_DIR/venv"
        return 0
    fi

    info "Creating Python virtual environment..."
    python3 -m venv "$PROJECT_DIR/venv"
    info "Virtual environment created"
}

# --- Activate and install dependencies ---

install_dependencies() {
    # Source the activation script
    # shellcheck source=/dev/null
    source "$PROJECT_DIR/venv/bin/activate"

    info "Upgrading pip..."
    pip install --upgrade pip setuptools wheel

    info "Installing dependencies from requirements.txt..."
    if [ -f "$PROJECT_DIR/scripts/requirements.txt" ]; then
        pip install -r "$PROJECT_DIR/scripts/requirements.txt"
        info "Dependencies installed successfully"
    else
        error "requirements.txt not found at $PROJECT_DIR/scripts/requirements.txt"
        return 1
    fi
}

# --- Verify installation ---

verify_installation() {
    # shellcheck source=/dev/null
    source "$PROJECT_DIR/venv/bin/activate"

    info "Verifying installed packages..."
    pip list | head -30
    echo ""
    info "Installation complete!"
}

# --- Main ---

echo ""
echo "========================================="
echo "  AI Study Repository Setup"
echo "========================================="
echo ""

if ! check_python; then
    error "Python 3 is required. Install from https://www.python.org/"
    exit 1
fi

if ! check_pip; then
    error "pip3 is required"
    exit 1
fi

setup_venv
install_dependencies
verify_installation

echo ""
info "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source $PROJECT_DIR/venv/bin/activate"
echo ""
echo "  2. Start working:"
echo "     cd $PROJECT_DIR"
echo "     jupyter notebook"
echo ""
echo "  3. Deactivate when done:"
echo "     deactivate"
echo ""
