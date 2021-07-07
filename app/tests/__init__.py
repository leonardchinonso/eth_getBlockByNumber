# The following lines execute system commands that run the python files in the tests' directories

import os

# Models
os.system("python app/tests/models/block/test_block_initialisation.py")
os.system("python app/tests/models/block/test_get_next_block.py")
os.system("python app/tests/models/block/test_get_prev_block.py")
os.system("python app/tests/models/block/test_set_next_block.py")
os.system("python app/tests/models/block/test_set_prev_block.py")

os.system("python app/tests/models/cache/test_add_to_head.py")
os.system("python app/tests/models/cache/test_cache_initialisation.py")
os.system("python app/tests/models/cache/test_get_block_by_number.py")
os.system("python app/tests/models/cache/test_get_head.py")
os.system("python app/tests/models/cache/test_is_full.py")
os.system("python app/tests/models/cache/test_remove_block.py")
os.system("python app/tests/models/cache/test_remove_tail.py")


# Controllers
os.system("python app/tests/controllers/blockController/test_get_block.py")
os.system("python app/tests/controllers/blockController/test_get_block_by_number.py")
os.system("python app/tests/controllers/blockController/test_get_block_from_cloud_flare.py")

os.system("python app/tests/controllers/transactionController/test_get_transaction_by_hash_value.py")
os.system("python app/tests/controllers/transactionController/test_get_transaction_by_index.py")


# Routes
os.system("python app/tests/routes/test_routes.py")


# Services
os.system("python app/tests/services/cacheService/test_get_cache.py")
os.system("python app/tests/services/cacheService/test_is_within_latest_block.py")

os.system("python app/tests/services/utilService/test_convert_hex_to_int.py")
os.system("python app/tests/services/utilService/test_is_hash.py")
