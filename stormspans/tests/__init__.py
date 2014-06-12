import os
import imp
import unittest

from glob import iglob

def find_tests():
    for path in iglob(os.path.dirname(os.path.realpath(__file__)) + "/test_*.py"):
        name = os.path.basename(path)[:-3]
        yield unittest.defaultTestLoader.loadTestsFromModule(
            imp.load_source(__name__ + "." + name, path))

def test_suite():
    return unittest.TestSuite(find_tests())

def main():
    runner = unittest.TextTestRunner(verbosity=1)
    return runner.run(unittest.TestSuite(find_tests()))
