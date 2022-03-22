"""
.. include:: ../../README.md
"""

from .shorten import shorten
from .lengthen import lengthen
from .consensus import consensus
from .to_html import to_html
from .mask import mask


# import os
# import glob

# dir_init = glob.glob(os.path.join("src","*","__init__.py"))[0]
# dir_init = os.path.dirname(dir_init)

# modules = [f for f in os.listdir(dir_init) if not f.startswith("__")]
# __all__ = [module.strip(".py") for module in modules]
# print(__all__)
