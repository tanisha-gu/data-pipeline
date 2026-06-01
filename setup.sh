#!/bin/bash

# Data Pipeline Setup Script
# Quick setup for Unix/Linux/macOS

echo "🚀 Data Pipeline Setup"
echo "====================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python $(python3 --version) found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created and activated"

# Install requirements
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Copy .env file
echo ""
echo "📝 Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (please edit with your MySQL credentials)"
else
    echo "✓ .env file already exists"
fi

# Create required directories
echo ""
echo "📁 Creating directories..."
mkdir -p data/raw
mkdir -p output/visualizations
mkdir -p logs

echo "✓ Directories created"

echo ""
echo "====================="
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env with your MySQL credentials"
echo "2. Place CSV files in data/raw/"
echo "3. Run: python main.py"
echo ""
echo "📚 For more help, see README.md"
