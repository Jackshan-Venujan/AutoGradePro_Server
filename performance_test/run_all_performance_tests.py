"""
Run All Performance Tests
Executes all performance tests and generates comprehensive report.

Run: python run_all_performance_tests.py
"""

import subprocess
import sys
import time
from pathlib import Path


def run_test(test_name, script_name):
    """Run a single test script"""
    print("\n" + "="*80)
    print(f"Running: {test_name}")
    print("="*80)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✅ {test_name} completed successfully")
            return True
        else:
            print(f"\n❌ {test_name} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"\n❌ Error running {test_name}: {str(e)}")
        return False


def main():
    """Run all performance tests"""
    print("\n" + "="*80)
    print("AUTOGRADEPRO - COMPLETE PERFORMANCE TEST SUITE")
    print("="*80)
    print("\nThis will run all performance tests:")
    print("  1. Grading Speed Test")
    print("  2. Throughput Test")
    print("  3. Concurrent Users Test")
    print("\nResults will be saved to: performance_test/results/")
    print("="*80)
    
    start_time = time.time()
    
    # Run all tests
    tests = [
        ("Grading Speed Test", "test_grading_speed.py"),
        ("Throughput Test", "test_throughput.py"),
        ("Concurrent Users Test", "test_concurrent_users.py")
    ]
    
    results = {}
    for test_name, script_name in tests:
        results[test_name] = run_test(test_name, script_name)
    
    total_time = time.time() - start_time
    
    # Print summary
    print("\n" + "="*80)
    print("COMPLETE PERFORMANCE TEST SUMMARY")
    print("="*80)
    
    print(f"\n📊 Test Results:")
    print("-" * 80)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n⏱️  Total Test Time: {total_time:.2f} seconds")
    
    # Check if all passed
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80)
        print("\n📄 Results Available:")
        print("-" * 80)
        results_dir = Path(__file__).parent / 'results'
        print(f"  📁 {results_dir}")
        print("  📝 grading_speed_results.json")
        print("  📝 throughput_results.json")
        print("  📝 concurrent_users_results.json")
        print("\n📋 Comprehensive Report:")
        print("-" * 80)
        report_file = Path(__file__).parent / 'PERFORMANCE_TEST_REPORT.md'
        print(f"  📄 {report_file}")
        print("\n✅ System is production-ready with proven performance!")
    else:
        print("\n" + "="*80)
        print("⚠️  SOME TESTS FAILED")
        print("="*80)
        print("\nPlease review the test output above for details.")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
