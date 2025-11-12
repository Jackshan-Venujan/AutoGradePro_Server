"""
Test Script - Verify Performance Time Test Setup
Run this to check if everything is configured correctly
"""

import os
import sys
from pathlib import Path

def check_file(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False

def check_django_setup():
    """Check if Django backend files exist"""
    print("\n" + "="*60)
    print("🔍 Checking Backend Setup (Django)")
    print("="*60)
    
    checks = [
        ("../Server/api/views.py", "Django views file"),
        ("../Server/api/urls.py", "Django URLs file"),
        ("../Server/api/functions.py", "Grading functions file"),
        ("timed_views.py", "Timed views (performance_time_test)"),
    ]
    
    results = [check_file(path, desc) for path, desc in checks]
    
    if all(results):
        print("\n✨ Backend files found!")
        print("\n📝 Next steps:")
        print("   1. Add timing endpoints to Server/api/urls.py")
        print("   2. Or patch your existing views with timing code")
        print("   3. See INTEGRATION_GUIDE.py for examples")
    else:
        print("\n⚠️  Some backend files are missing")
    
    return all(results)

def check_frontend_setup():
    """Check if frontend files exist"""
    print("\n" + "="*60)
    print("🔍 Checking Frontend Setup (React)")
    print("="*60)
    
    checks = [
        ("performance_logger_component.jsx", "Performance Logger component"),
        ("grading_api_with_timing.js", "API client with timing"),
        ("performance_logger.css", "Performance Logger styles"),
    ]
    
    results = [check_file(path, desc) for path, desc in checks]
    
    if all(results):
        print("\n✨ Frontend files ready!")
        print("\n📝 Next steps:")
        print("   1. Copy these files to your Client/app folder")
        print("   2. Import PerformanceLogger in your layout")
        print("   3. Replace API calls with timed versions")
        print("   4. See QUICKSTART.md for detailed steps")
    else:
        print("\n⚠️  Some frontend files are missing")
    
    return all(results)

def check_analysis_tools():
    """Check if analysis tools exist"""
    print("\n" + "="*60)
    print("🔍 Checking Analysis Tools")
    print("="*60)
    
    checks = [
        ("collect_metrics.py", "Metrics collection script"),
        ("README.md", "Documentation"),
        ("QUICKSTART.md", "Quick start guide"),
        ("INTEGRATION_GUIDE.py", "Integration examples"),
    ]
    
    results = [check_file(path, desc) for path, desc in checks]
    
    if all(results):
        print("\n✨ Analysis tools ready!")
        print("\n📝 Usage:")
        print("   python collect_metrics.py <exported_json_file>")
    
    return all(results)

def print_summary():
    """Print setup summary"""
    print("\n" + "="*60)
    print("📋 SETUP SUMMARY")
    print("="*60)
    
    print("""
This folder contains:

📁 Backend (Django):
   - timed_views.py - API views with performance timing
   
📁 Frontend (React):
   - performance_logger_component.jsx - Real-time metrics display
   - grading_api_with_timing.js - API client with timing
   - performance_logger.css - Styling
   
📁 Analysis:
   - collect_metrics.py - Analyze exported metrics
   
📁 Documentation:
   - README.md - Full documentation
   - QUICKSTART.md - 5-minute setup guide
   - INTEGRATION_GUIDE.py - Code examples

🚀 Quick Start:
   1. Read QUICKSTART.md (5 min setup)
   2. Add timing to your backend
   3. Add PerformanceLogger to frontend
   4. Grade assignments and collect data
   5. Export metrics and analyze

🎯 Goal:
   Get real performance data for your abstract/research paper:
   - One-word: <1ms
   - List: 1-5ms  
   - Numerical: <1ms
   - Short-phrase: 2-5s (with AI)
""")

def main():
    """Main test function"""
    print("="*60)
    print("🧪 Performance Time Test - Setup Verification")
    print("="*60)
    
    backend_ok = check_django_setup()
    frontend_ok = check_frontend_setup()
    analysis_ok = check_analysis_tools()
    
    print_summary()
    
    if backend_ok and frontend_ok and analysis_ok:
        print("\n✅ All files present! Ready to integrate.")
        print("👉 Start with QUICKSTART.md")
        return 0
    else:
        print("\n⚠️  Some files are missing, but core files are present.")
        print("👉 You can still use the available tools")
        return 1

if __name__ == "__main__":
    sys.exit(main())
