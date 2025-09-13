#!/bin/bash
# TEF-2025 Setup and Run Script

set -e

echo "🔬 TEF-2025: Trilemma Evaluation Framework 2025"
echo "================================================"

# Check if we're in the right directory
if [[ ! -f "config.yaml" ]]; then
    echo "❌ Error: config.yaml not found. Run this script from the tef2025/ directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q numpy pandas matplotlib scipy pyyaml seaborn

# Validate CSV data
echo "🔍 Validating input data..."
python analysis/validate_csv.py inputs/results.csv

# Run analysis
echo "🚀 Running TEF-2025 analysis..."
python analysis/tef2025_analysis.py --input inputs/results.csv --outdir outputs --config config.yaml

echo ""
echo "✅ Analysis complete!"
echo "📁 Results saved to: outputs/"
echo "📊 View report: outputs/report.md"
echo "🎨 Charts: outputs/*.png"
echo "📈 Data: outputs/results_normalized.csv"
