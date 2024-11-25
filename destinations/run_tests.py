import unittest
import coverage
import os
import sys

def run_tests():
    """Run tests with coverage"""
    # Configure coverage
    cov = coverage.Coverage(
        branch=True,
        source=['destinations'],
        omit=[
            '*/site-packages/*',
            '*/tests/*',
            '*/__pycache__/*',
            '*/__init__.py'
        ]
    )
    
    # Start coverage
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    
    # Stop coverage
    cov.stop()
    cov.save()
    
    # Report coverage
    print('\nCoverage Summary:')
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory='coverage_report')
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 