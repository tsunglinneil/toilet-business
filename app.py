# coding=utf-8

# possible need it:
# import os
# import sys
# print(os.path.dirname(__name__))
# sys.path.append(os.path.dirname(__name__))

from toilet_business import create_app

if __name__ == "__main__":
    create_app().run()
