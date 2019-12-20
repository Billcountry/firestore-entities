import unittest
import sys
import os


if __name__ == "__main__":
    # Add main dir to path
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
    suite = unittest.loader.TestLoader().discover(os.path.dirname(__file__), "test_*")
    result = unittest.runner.TextTestRunner().run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
