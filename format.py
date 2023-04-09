def auto_digits(x):
    digits = 0
    if x < 0:
        x *= -1
    while x < 1:
        x *= 10
        digits += 1
    while x >= 10:
        x /= 10
        digits -= 1
    if x <= 3:
        digits += 1
    return digits

def exponent(x):
    power = 0
    if x < 0:
        x *= -1
    while x < 1:
        x *= 10
        power += 1
    while x >= 10:
        x /= 10
        power -= 1
    return power

def nice(x, digits=None):
    sign = ""
    if x < 0:
        sign = "-"
        x *= -1
    if digits is None:
        digits = auto_digits(x)
    if digits <= 0:
        digits *= -1
        x = round(x / 10 ** digits) * 10 ** digits
        return str(x)
    x = round(x * 10 ** digits)
    r = str(x % 10 ** digits)
    r = "0" * (digits - len(r)) + r
    return sign + str(x // 10 ** digits) + "." + r

def nice_arr(x, digits=None, units=1):
    return [nice(x_i / units, digits) for x_i in x]
