# coding=utf-8

# possible need it:
# import os
# import sys
# print(os.path.dirname(__name__))
# sys.path.append(os.path.dirname(__name__))

from toilet_business import create_app
from toilet_business import leveldb_util

if __name__ == "__main__":
    db = leveldb_util.init('toilet_db')
    create_app().run()
