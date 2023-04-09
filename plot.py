import matplotlib.pyplot as plt
import numpy as np

from val import Val, valarray
from utils import load

# Helper function to create Val object for k returned by polyfit
# Absolute error taken from delta argument
# Poly and delta should be returned by polyfit
def k_polyfit(poly, delta):
    return Val(poly[0], delta[0][0] ** 0.5)

def get_ax():
    return plt.subplots(figsize=(10, 10))[1]

# TODO: move into plot.py module
class Plot:
   
    default_params = {
        "color": "dimgrey",
        "trendcolor": "lightgray",
        "fmt": ".",
        "label": None,
        "xlabel": None,
        "ylabel": None,
        "xlims": None,
        "ylims": None,
        "xrange": None,
        "ax": None,
        "fontsize_text": 32,
        "fontsize_ticks": 18,
        "trendwidth": 2,
        "errorwidth": 1.5,
        "markersize": 8,
        "linestyle": None,
        "legendsize": 16
    }

    def capture(self, **kwargs):
        unrecognized_params = {}
        for param in kwargs:
            if param in self.default_params:
                self.__dict__[param] = kwargs[param]
            else:
                unrecognized_params[param] = kwargs[param]
        return unrecognized_params
    
    def capturing(function):
        ''' Decorator which allows a function to take any number of
        named arguments corresponding to default params which will set them
        '''
        def capturing_function(self, *args, **kwargs):
            function_params = self.capture(**kwargs)
            return function(self, *args, **function_params)
        return capturing_function
    
    def set_defaults(self):
        for param in self.default_params:
            if not param in self.__dict__:
                self.__dict__[param] = self.default_params[param]

    @classmethod
    def load(cls, filename='data', transpose=True, **kwargs):
        ''' Loads X and Y from a file and returns a Plot object '''
        dump = load(filename=filename, transpose=transpose)
        if len(dump) != 2:
            print("Warning: More than 2 values detected, extras are discarded")
        return cls(X=dump[0], Y=dump[1], **kwargs)
    
    @capturing
    def __init__(self, X, Y, dX=0, dY=0):
        ''' '''
        if isinstance(X[0], Val):
            dX = [val.delta for val in X]
            X = [val.value for val in X]
        if isinstance(Y[0], Val):
            dY = [val.delta for val in Y]
            Y = [val.value for val in Y]
        self.X = X
        self.Y = Y
        self.dX = dX
        self.dY = dY
        self.set_defaults()
        if type(self.xrange) is tuple or type(self.xrange) is list and self.xlims is None:
            self.xlims = (self.xrange[0], self.xrange[-1])
        poly, delta = np.polyfit(X, Y, 1, cov=True)
        self.k = k_polyfit(poly, delta)
        self.p = np.poly1d(poly)
        self.show()
        if not self.xrange is None:
            self.trend()
    
    def ensure_ax(self):
        if self.ax is None:
            print("No axis provided, creating new figure")
            _, self.ax = plt.subplots(figsize=(10, 10))

    @capturing
    def show(self):
        self.ensure_ax()
        self.ax.errorbar(self.X, self.Y, xerr=self.dX, yerr=self.dY, fmt=self.fmt, color=self.color, label=self.label, linewidth=self.errorwidth, markersize=self.markersize)
        self.meta()

    @capturing
    def trend(self):
        ''' Displays trendline '''
        if self.xrange is None:
            print("Error: No xrange specified")
            return
        self.ensure_ax()
        self.ax.plot(self.xrange, self.p(self.xrange), color=self.trendcolor, linestyle=self.linestyle, linewidth=self.trendwidth)
        self.meta()
    
    @capturing
    def meta(self):
        self.ensure_ax()
        if self.xlims is not None:
            self.ax.set_xlim(*self.xlims)
        if self.ylims is not None:
            self.ax.set_ylim(*self.ylims)
        if self.xlabel is not None:
            self.ax.set_xlabel(self.xlabel, loc='center', fontsize=self.fontsize_text)
        if self.ylabel is not None:
            self.ax.set_ylabel(self.ylabel, loc='center', fontsize=self.fontsize_text)
        self.ax.tick_params(axis='both', which='major', labelsize=self.fontsize_ticks)
        self.ax.grid(which='major', alpha = 0.1, color = "black")
        if self.label is not None:
            self.ax.legend(fontsize=self.legendsize)
    
    @capturing 
    def recalc(self, force_zero=True, ind=None):
        ''' Recalculates trend taking into account only points with ind indicies'''
        X = self.X
        Y = self.Y
        if ind is not None:
            X = self.X[ind]
            Y = self.Y[ind]
        if force_zero:
            X = np.append(X, np.array([0]))
            Y = np.append(Y, np.array([0]))
        poly, delta = np.polyfit(X, Y, 1, cov=True)
        self.k = k_polyfit(poly, delta)
        self.p = np.poly1d(poly)
        self.trend()
