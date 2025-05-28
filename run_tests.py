#!/usr/bin/env python3
"""
Test runner for all stages of the SimpleWebScraper project.

This script runs unit tests for all stages and provides a summary of results.
"""

import unittest
import sys
import os
from pathlib import Path


def discover_and_run_tests():
    """Discover and run all test files in the project."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Results storage
    all_results = []
    
    # Test each stage
    stages = ['stage1', 'stage2', 'stage3', 'stage4']
    
    for stage in stages:
        stage_dir = project_root / stage
        if not stage_dir.exists():
            print(f"Warning: {stage} directory not found, skipping...")
            continue
            
        print(f"\n{'='*50}")
        print(f"Running tests for {stage.upper()}")
        print(f"{'='*50}")
        
        # Add stage directory to Python path
        sys.path.insert(0, str(stage_dir))
        
        try:
            # Discover tests in the stage directory
            loader = unittest.TestLoader()
            suite = loader.discover(str(stage_dir), pattern='test_*.py')
            
            # Run the tests
            runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
            result = runner.run(suite)
            
            # Store results
            all_results.append({
                'stage': stage,
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'success': result.wasSuccessful()
            })
            
        except Exception as e:
            print(f"Error running tests for {stage}: {e}")
            all_results.append({
                'stage': stage,
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'success': False
            })
        
        # Remove from path to avoid conflicts
        if str(stage_dir) in sys.path:
            sys.path.remove(str(stage_dir))
    
    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for result in all_results:
        status = "✓ PASSED" if result['success'] else "✗ FAILED"
        print(f"{result['stage'].upper():<10} | {result['tests_run']:>2} tests | "
              f"{result['failures']:>2} failures | {result['errors']:>2} errors | {status}")
        
        total_tests += result['tests_run']
        total_failures += result['failures']
        total_errors += result['errors']
    
    print(f"{'-'*50}")
    print(f"{'TOTAL':<10} | {total_tests:>2} tests | "
          f"{total_failures:>2} failures | {total_errors:>2} errors")
    
    # Overall result
    overall_success = total_failures == 0 and total_errors == 0
    if overall_success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ Tests failed: {total_failures} failures, {total_errors} errors")
        return 1


if __name__ == '__main__':
    sys.exit(discover_and_run_tests())
