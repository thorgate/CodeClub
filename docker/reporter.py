import os
import json
import unittest
from time import time

SECRET = os.environ.pop("KEY")

from tester import *


class JSONTestResult(unittest.TextTestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.test_start = None
        self.test_times = {}
        self.success = []

    def startTest(self, test):
        self.startTimer(test)
        unittest.TestResult.startTest(self, test)

    def startTimer(self, test):
        self.test_start = time()

    def endTimer(self, test):
        self.test_times[test] = time() - self.test_start

    def addError(self, test, err):
        self.endTimer(test)
        super().addError(test, err)

    def addExpectedFailure(self, test, err):
        self.endTimer(test)
        super().addExpectedFailure(test, err)

    def addFailure(self, test, err):
        self.endTimer(test)
        super().addFailure(test, err)

    def addSkip(self, test, reason):
        self.endTimer(test)
        super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        self.endTimer(test)
        super().addSubTest(test, subtest, err)

    def addSuccess(self, test):
        self.endTimer(test)
        super().addSuccess(test)
        # TestRunner drops successful tests
        self.success.append(test)

    def addUnexpectedSuccess(self, test):
        self.endTimer(test)
        super().addUnexpectedSuccess(test)

    def printErrors(self):
        super().printErrors()
        result = []
        for test in self.success:
            result.append(self.serialize(test, self.test_times.get(test), 'SUCCESS', None))

        for test, err in self.failures:
            result.append(self.serialize(test, self.test_times.get(test), 'FAIL', str(err)))

        for test, err in self.errors:
            result.append(self.serialize(test, self.test_times.get(test), 'ERROR', str(err)))

        data = {
            'key': SECRET,
            'tests': result,
            'fail': len(self.failures),
            'success': len(self.success),
            'error': len(self.errors),
        }
        with open("/mount/report.txt", "w") as outfile:
            json.dump(data, outfile)

    def serialize(self, test, time, flavor, err):
        data = {
            'test': str(self.getDescription(test).split()[0]),
            'seconds': time,
            'flavor': flavor,
            'error': err
        }
        return data


if __name__ == '__main__':
     unittest.main(exit=False, testRunner=unittest.TextTestRunner(resultclass=JSONTestResult))
