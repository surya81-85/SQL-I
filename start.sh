#!/bin/bash

echo "=================================="
echo "Flask SQLite3 Auth System Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

echo ""
echo "Installing dependencies..."
pip install flask flask-cors --break-system-packages

echo ""
echo "=================================="
echo "Starting Flask Application..."
echo "=================================="
echo ""
echo "Access the app at: http://localhost:5000"
echo ""
echo "Demo credentials:"
echo "  Username: admin"
echo "  Password: demo123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
python3 app.py
