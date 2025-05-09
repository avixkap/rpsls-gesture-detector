# run_tests.py
import unittest
import HtmlTestRunner
import os

# Discover tests in the 'tests' folder
loader = unittest.TestLoader()
suite = loader.discover('tests')

# Run tests with HtmlTestRunner
runner = HtmlTestRunner.HTMLTestRunner(
    output='tests/test-reports',
    report_title='RPS Test Report',
    descriptions=True
)
runner.run(suite)
