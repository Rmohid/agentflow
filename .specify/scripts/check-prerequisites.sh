#!/bin/bash
# Check prerequisites for AgentFlow development
# Usage: ./check-prerequisites.sh

set -e

echo "Checking AgentFlow prerequisites..."
echo ""

MISSING=0

# Check Python
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    echo "✓ Python ${VERSION} found"
else
    echo "✗ Python 3.10+ required"
    MISSING=1
fi

# Check pip
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    echo "✓ pip found"
else
    echo "✗ pip required"
    MISSING=1
fi

# Check git
if command -v git &> /dev/null; then
    echo "✓ git found"
else
    echo "✗ git required"
    MISSING=1
fi

# Check virtual environment
if [ -d ".venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "⚠ Virtual environment not found (run: python -m venv .venv)"
fi

# Check dependencies installed
if [ -f "pyproject.toml" ]; then
    if python3 -c "import fastapi" 2>/dev/null; then
        echo "✓ Dependencies installed"
    else
        echo "⚠ Dependencies not installed (run: pip install -e '.[dev]')"
    fi
fi

# Check .specify structure
if [ -d ".specify/memory" ] && [ -f ".specify/memory/constitution.md" ]; then
    echo "✓ Spec Kit structure present"
else
    echo "⚠ Spec Kit structure incomplete"
fi

echo ""
if [ $MISSING -eq 0 ]; then
    echo "All prerequisites satisfied!"
else
    echo "Some prerequisites missing. Please install them."
    exit 1
fi
