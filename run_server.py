#!/usr/bin/env python
"""
Startup script untuk RJPP Novelty Detection System
"""

import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("RJPP Novelty Detection System")
    print("=" * 50)
    print()
    
    # Install dependencies if needed
    print("Installing/updating dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
    
    print()
    print("=" * 50)
    print("Starting server on http://127.0.0.1:8000")
    print("=" * 50)
    print()
    print("Interface: http://127.0.0.1:8000/interface")
    print("API Docs:  http://127.0.0.1:8000/docs")
    print("Health:    http://127.0.0.1:8000/health")
    print()
    print("Press CTRL+C to stop the server")
    print()
    
    # Start uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)
