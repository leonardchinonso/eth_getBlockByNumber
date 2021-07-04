import os
import sys
print("os path", os.path.dirname(__file__))

topdir = os.path.join(os.path.dirname("C:\\Users\\USER\\Projects\\Personal\\eth_getBlockByNumber\\testingTest.py"), "..")
sys.path.append(topdir)
print("sys path", sys.path)

from app import app
import unittest

class TestTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/block/latest", content_type="html/text")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
