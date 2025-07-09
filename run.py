#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import signal

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors"], check=True)

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("Installing frontend dependencies...")
    os.chdir("frontend")
    subprocess.run(["npm", "install"], check=True)
    os.chdir("..")

def build_frontend():
    """Build React frontend"""
    print("Building React frontend...")
    os.chdir("frontend")
    subprocess.run(["npm", "run", "build"], check=True)
    os.chdir("..")

def run_flask_app():
    """Run Flask application"""
    print("Starting Flask application...")
    os.environ['FLASK_ENV'] = 'development'
    subprocess.run([sys.executable, "app.py"])

def main():
    try:
        # Install dependencies
        install_dependencies()
        
        # Check if npm is available
        try:
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            install_frontend_dependencies()
            build_frontend()
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("npm not found. Please install Node.js and npm first.")
            print("For now, running without frontend build...")
        
        # Run Flask app
        run_flask_app()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()