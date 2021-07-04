import os
import sys
import json
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services.errorService import ErrorHandler
from app.services import cacheService as CacheService


# WARNING: Running the tests below will modify current contents of "app/models/cache.json".
# To run the tests:
# Comment the skip code lines above each test method.
class TestWriteToCache(unittest.TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(os.getenv("BASE_PATH"), "app/models/cache.json")
        self.test_data = {
            "test_cache": "contains information again"
        }

    @unittest.skip("Skipped 1 test")
    def test_write_to_cache_is_successful(self):
        CacheService.write_to_cache_file(self.test_data)

        try:
            cache_file = open(self.path, "r")
        except FileNotFoundError:
            raise ErrorHandler("File for cache does not exist!", 500)

        data = cache_file.read()

        cache_file.close()

        records = json.loads(data)

        self.assertEqual(self.test_data, records)


if __name__ == "__main__":
    unittest.main()
