import coverage
import unittest

cov = coverage.coverage()
cov.start()

tests = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(tests)
cov.stop()
cov.report()
cov.html_report(directory='test_report')