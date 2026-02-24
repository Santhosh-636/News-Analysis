#!/usr/bin/env python3
"""
Quick Start Script - Indian News Sentiment Analysis Dashboard
Run this to start everything automatically
"""

import subprocess
import sys
import time
import webbrowser

def main():
    print("\n" + "="*70)
    print(" "*15 + "NEWS SENTIMENT ANALYSIS DASHBOARD")
    print(" "*20 + "Quick Start")
    print("="*70 + "\n")
    
    print("🚀 Starting the dashboard...\n")
    
    # Get Python executable path
    python_exe = ".venv\\Scripts\\python.exe"
    
    try:
        # Start streamlit
        print("📊 Launching Streamlit server...")
        process = subprocess.Popen(
            [python_exe, "-m", "streamlit", "run", "dashboard.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("⏳ Waiting for server to start...")
        time.sleep(5)  # Wait for server to start
        
        print("✓ Streamlit server started!")
        print("\n" + "="*70)
        print("📍 DASHBOARD READY:")
        print("="*70)
        print("   Local URL: http://localhost:8501")
        print("   Network URL: http://10.39.12.48:8501")
        print("="*70 + "\n")
        
        # Open browser
        print("🌐 Opening dashboard in your browser...")
        webbrowser.open("http://localhost:8501")
        
        print("\n✅ Dashboard is now running!")
        print("   The dashboard will remain active until you close this terminal.")
        print("   Press Ctrl+C to stop the server.\n")
        
        # Keep the server running
        process.wait()
        
    except FileNotFoundError:
        print("❌ Error: Python executable not found.")
        print("   Make sure you're running this from the project directory.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down dashboard...")
        process.terminate()
        process.wait()
        print("✓ Dashboard stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
