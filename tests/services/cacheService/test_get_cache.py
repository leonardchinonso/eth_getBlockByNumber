import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services.errorService import ErrorHandler
from app.services import cacheService as CacheService


# WARNING: Running the tests below will overwrite current contents of "app/models/cache.json".
# To run the tests:
# Comment the skip code lines above each test method.
# Uncomment every other commented lines.
class TestGetCache(unittest.TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(os.getenv("BASE_PATH"), "app/models/cache.json")
        # self.test_file = open(self.path, "w")

    def tearDown(self) -> None:
        # self.test_file.close()
        pass

    @unittest.skip("Skipped 1 test")
    def test_get_cache_returns_empty_dict(self):
        self.assertEqual(CacheService.get_cache(), {})

    @unittest.skip("Skipped 1 test")
    def test_get_cache_returns_a_valid_dict(self):
        test_data = {
            "test_cache": "contains information now"
        }
        # json.dump(test_data, self.test_file)
        # self.test_file.close()
        self.assertEqual(CacheService.get_cache(), test_data)


if __name__ == "__main__":
    unittest.main()
