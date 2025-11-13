#!/usr/bin/env bash
# VolcoGUI First Launch Script
# This script will set up and run VolcoGUI for the first time

echo "=================================="
echo "  VolcoGUI - First Launch Setup"
echo "=================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: 'uv' is not installed"
    echo ""
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

echo "✓ uv is installed"
echo ""

# Sync dependencies
echo "📦 Installing dependencies..."
echo "   This may take 2-3 minutes on first run..."
echo ""
uv sync

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully"
echo ""

# Check if Volco is available
echo "🔍 Checking for Volco installation..."
if uv pip show volco &> /dev/null; then
    echo "✓ Volco is installed"
    VOLCO_INSTALLED=true
else
    echo "⚠️  Volco is not installed"
    echo "   App will run in TEST MODE (creates test cube)"
    echo ""
    echo "   To install Volco:"
    echo "   uv pip install -e /path/to/volco"
    echo ""
    VOLCO_INSTALLED=false
fi

echo ""
echo "=================================="
echo "  Launching VolcoGUI..."
echo "=================================="
echo ""

# Launch the application
uv run python -m volcogui.main

echo ""
echo "Application closed."
echo ""

if [ "$VOLCO_INSTALLED" = false ]; then
    echo "💡 Tip: Install Volco for full functionality:"
    echo "   uv pip install -e /path/to/volco"
    echo ""
fi
