import pprint

import inspect
def proc():
  pprint.pprint( inspect.stack() )


import sys
def proc():
  print( sys._getframe().f_code.co_name )


import traceback

