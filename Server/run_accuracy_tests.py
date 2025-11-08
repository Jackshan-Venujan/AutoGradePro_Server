#!/usr/bin/env python
"""
Quick Test Runner for AutoGradePro Grading Accuracy
Run this script directly: python run_accuracy_tests.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')
django.setup()

from django.test.utils import get_runner
from django.conf import settings

if __name__ == "__main__":
    print("="*70)
    print("AutoGradePro Grading Accuracy Tests")
    print("="*70)
    print("\nRunning all grading accuracy tests...\n")

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)

    # Run only the grading accuracy tests
    failures = test_runner.run_tests(["tests.test_grading_accuracy"])

    if failures:
        print(f"\n❌ {failures} test(s) failed")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)