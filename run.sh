#!/bin/bash
# Run RJPP Novelty Detection System

echo "RJPP Novelty Detection System"
echo "============================"
echo ""
echo "Instalasi dependensi..."
pip install -r requirements.txt

echo ""
echo "Starting server pada http://127.0.0.1:8000"
echo "Interface: http://127.0.0.1:8000/interface"
echo "API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Tekan CTRL+C untuk menghentikan server"
echo ""

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
