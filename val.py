import numpy as np

from format import nice, auto_digits, exponent
from utils import copy_to_clipboard

class Val:

    def nonzero(self):
        return abs(self.value) > 1e-20

    def __init__(self, value, delta=0, eps=0):
        self.value = value
        self.delta = delta
        self.eps = eps

        if self.delta == 0:
            self.delta = abs(value * eps)
        if self.eps == 0:
            if self.nonzero():
                self.eps = abs(delta / value)
            else:
                self.eps = float("inf")

    @classmethod
    def cast(cls, x):
        if isinstance(x, Val):
            return x
        if isinstance(x, (int, float)):
            return Val(x)
        if isinstance(x, (list, tuple)):
            if len(x) == 2:
                return Val(x[0], x[1])
            else:
                raise Exception("Bad cast, list len is not 2")
        raise Exception("Bad cast, unsupported type")
    
    def __add__(self, other):
        if not isinstance(other, Val):
            return self + Val.cast(other)
        return Val(self.value + other.value, delta=(self.delta ** 2 + other.delta ** 2) ** 0.5)

    def __neg__(self):
        return Val(-self.value, self.delta)
    
    def __sub__(self, other):
        if not isinstance(other, Val):
            return self - Val.cast(other)
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Val):
            return self * Val.cast(other)
        if self.nonzero() and other.nonzero():
            return Val(self.value * other.value, eps=(self.eps**2 + other.eps ** 2) **0.5)
        else:
            return Val(0, 0)

    def _rev(self):
        return Val(1 / self.value, eps=self.eps)
    
    def __truediv__(self, other):
        if not isinstance(other, Val):
            return self / Val.cast(other)
        return self * other._rev()

    def __pow__(self, power):
        return Val(self.value ** power, eps=abs(power * self.eps))
    
    def _val_str(self):
        if not self.nonzero():
            return "0"
        exp = exponent(self.value)
        digits = auto_digits(self.delta)
        if abs(exp) < 3:
            return f"{nice(self.value, digits)} \\pm {nice(self.delta)}"
        value = self.value * 10 ** exp
        delta = self.delta * 10 ** exp
        return f"({nice(value, digits-exp)} \\pm {nice(delta)}) \\cdot 10^" + "{" +f"{-exp}" + "}"

    def __str__(self):
        if not self.nonzero():
            return "0"
        if self.delta < 1e-20:
            return nice(self.value)
        return f"${self._val_str()}$ units, $(\\varepsilon = {nice(100 * self.eps)}\\%)$"
    
    def val_str(self):
        if not self.nonzero():
            return f"0 ± {self.delta}"
        exp = exponent(self.value)
        digits = auto_digits(self.delta)
        if abs(exp) < 3:
            return f"{nice(self.value, digits)} ± {nice(self.delta)}"
        value = self.value * 10 ** exp
        delta = self.delta * 10 ** exp
        return f"({nice(value, digits-exp)} ± {nice(delta)}) × 1e{-exp}"

    def __repr__(self):
        if not self.nonzero():
            return f"<Val: {self.val_str()}>"
        if self.eps < 1e-20:
            return f"<Val: exactly {nice(self.value)}>"
        copy_to_clipboard(self.__str__())
        return f"<Val: {self.val_str()}, eps = {nice(100 * self.eps)}%>"

    def latex(self):
        print(self.__str__())
        copy_to_clipboard(self.__str__())

def valarray(*args):
    return np.array([Val.cast(arg) for arg in args], dtype=np.dtype(Val))

def add_error(array, error):
    return np.array([Val(element, error) for element in array])
