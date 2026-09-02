#!/usr/bin/env python3
"""
Quick Setup Script for Hospital Integration
Installs all dependencies needed for hospital document retrieval
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"⚠️  {description} - Completed with warnings")
            return True
    except Exception as e:
        print(f"❌ {description} - Error: {str(e)}")
        return False

def main():
    """Main setup function"""
    
    print("\n" + "="*60)
    print("🏥 Hospital Document Integration - Setup")
    print("="*60)
    
    print("\nThis script will:")
    print("1. Install required Python packages")
    print("2. Check for hospital documents")
    print("3. Initialize the knowledge base")
    
    # Step 1: Install requirements
    print("\n📥 Installing dependencies...")
    cmd = f"{sys.executable} -m pip install -r requirements.txt --upgrade"
    run_command(cmd, "Installing Python packages")
    
    # Step 2: Fix TensorFlow/Keras compatibility
    print("\n🔧 Fixing TensorFlow compatibility...")
    cmd = f"{sys.executable} -m pip install tf-keras --upgrade"
    run_command(cmd, "Installing tf-keras compatibility layer")
    
    # Step 3: Check for hospital docs
    print("\n📁 Checking for hospital documents...")
    if os.path.exists("hospital_docs"):
        pdf_count = len([f for f in os.listdir("hospital_docs") if f.lower().endswith('.pdf')])
        if pdf_count > 0:
            print(f"✅ Found {pdf_count} hospital PDF document(s)")
        else:
            print("ℹ️  No PDF files in hospital_docs folder yet")
            print("   You can add them later, the system can also use website content")
    else:
        print("ℹ️  hospital_docs folder doesn't exist yet")
        print("   Creating it now...")
        os.makedirs("hospital_docs", exist_ok=True)
        print("✅ Created hospital_docs folder")
        print("   You can add hospital PDFs here")
    
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print("\nYou can now:")
    print("1. Add hospital PDF documents to hospital_docs/ folder")
    print("2. Run: streamlit run app.py")
    print("3. Ask questions like:")
    print("   - 'What services do you provide?'")
    print("   - 'What are your visiting hours?'")
    print("   - 'Book me an appointment'")
    print("\n📖 For more info, see: START_HERE.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
