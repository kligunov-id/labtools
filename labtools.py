# version 1.1.3
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython

from val import Val, valarray, add_error
from utils import load, transpose
from table import table
from format import nice, nice_arr
from units import *
from plot import Plot, get_ax, k_polyfit

# IPython should automatically detect backends for matplotlib,
# but on my setup it somehow doesn't
get_ipython().run_line_magic("matplotlib", "")

class ScripRunner:
    
    @staticmethod
    def add_extension(script_name):
        if len(script_name) >= 3 and script_name[-3:] == ".py":
            return script_name
        return script_name + ".py"

    def __call__(self, script_name="cache.py"):
        get_ipython().run_line_magic("run", f"-i {self.add_extension(script_name)}")
        # Somehow when scripts are executed via %run magick
        # plots don't show up automatically
        plt.show()

    def __repr__(self):
        ''' Allow to run script when typing run without ():
        Usage as follows:
        >>> run
        '''
        self.__call__()
        return ""

run = ScripRunner()
