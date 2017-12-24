# coding=utf-8

# possible need it:
# import os
# import sys
# print(os.path.dirname(__name__))
# sys.path.append(os.path.dirname(__name__))

import os
from toilet_business import create_app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    create_app().run(host='0.0.0.0', port=port)
