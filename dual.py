class Dual:
    def __init__(self, real, dual=0.0):
        self.real = real      # Value of the function
        self.dual = dual      # Derivative

    def __add__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real + other.real, self.dual + other.dual)
        return Dual(self.real + other, self.dual)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real - other.real, self.dual - other.dual)
        return Dual(self.real - other, self.dual)

    def __rsub__(self, other):
        return Dual(other - self.real, -self.dual)

    def __mul__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real * other.real,
                        self.real * other.dual + self.dual * other.real)
        return Dual(self.real * other, self.dual * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Dual):
            f = self.real / other.real
            d = (self.dual * other.real - self.real * other.dual) / (other.real ** 2)
            return Dual(f, d)
        return Dual(self.real / other, self.dual / other)

    def __rtruediv__(self, other):
        f = other / self.real
        d = -other * self.dual / (self.real ** 2)
        return Dual(f, d)

    def __pow__(self, power):
        f = self.real ** power
        d = power * self.real ** (power - 1) * self.dual
        return Dual(f, d)