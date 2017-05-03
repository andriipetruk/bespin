from bespin.errors import BespinError

from contextlib import contextmanager
import json
import sys

class NotSpecified(object):
    """Tell the difference between empty and None"""

class AssertionsAssertionsMixin:
    def assertSortedEqual(self, one, two):
        """Assert that the sorted of the two equal"""
        self.assertEqual(sorted(one), sorted(two))

    def assertJsonDictEqual(self, one, two):
        """Assert the two dictionaries are the same, print out as json if not"""
        try:
            self.assertEqual(one, two)
        except AssertionError:
            print("Got =============>")
            print(json.dumps(one, indent=2, sort_keys=True))
            print("Expected --------------->")
            print(json.dumps(two, indent=2, sort_keys=True))
            raise

    def assertItemsEqual(self, a, b):
        """wraps assertCountEqual, assertItemsEqual or poorly emulates it"""
        if sys.version_info[0] == 3 and sys.version_info[1] >= 2:
            return self.assertCountEqual(a, b)
        elif sys.version_info[0] == 2 and sys.version_info[1] >= 7:
            return self.assertItemsEqual(a, b)
        else:
            return self.assertEqual(sorted(a), sorted(b))

    @contextmanager
    def fuzzyAssertRaisesError(self, expected_kls, expected_msg_regex=NotSpecified, **values):
        """
        Assert that something raises a particular type of error.

        The error raised must be a subclass of the expected_kls
        Have a message that matches the specified regex.

        And have atleast the values specified in it's kwargs.
        """
        try:
            yield
        except BespinError as error:
            try:
                assert issubclass(error.__class__, expected_kls)
                if expected_msg_regex is not NotSpecified:
                    self.assertRegexpMatches(expected_msg_regex, error.message)

                errors = values.get("_errors")
                if "_errors" in values:
                    del values["_errors"]

                self.assertDictContainsSubset(values, error.kwargs)
                if errors:
                    self.assertEqual(sorted(error.errors), sorted(errors))
            except AssertionError:
                print("Got error: {0}".format(error))
                print("Expected: {0}: {1}: {2}".format(expected_kls, expected_msg_regex, values))
                raise
        else:
            assert False, "Expected an exception to be raised\n\texpected_kls: {0}\n\texpected_msg_regex: {1}\n\thave_atleast: {2}".format(
                expected_kls, expected_msg_regex, values
            )

