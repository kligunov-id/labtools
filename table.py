from utils import copy_to_clipboard

def _header(n, first_sep=True):
    column_manifest = "X" * n
    if first_sep:
        column_manifest = "l" + column_manifest
    return "\\medskip\\medskip \\hspace{0.05\\textwidth}\n\\begin{tabularx}{0.85\\textwidth}{" + column_manifest + "} \\toprule\n"

def _footer():
    return "\\bottomrule\n\\end{tabularx} \\medskip\\medskip"

def _mid(x, name=None, first_sep=True):
    if name is None:
        name = ""
    if first_sep:
        name = "    " + name
    return name + _row_table(x, first_sep=first_sep)

def _row_table(x, sep=" & ", first_sep=True, end="\\\\\n"):
    result = ""
    for i, el in enumerate(x):
        if i != 0 or first_sep:
            result += sep
        result += str(el) 
    return result + end

def table(list_arrays, list_names=None, output = "cr", first_sep=True):
    mid = ""
    if list_names is None:
        list_names = [None] * len(list_arrays)
    for array, name in zip(list_arrays, list_names):
        mid += _mid(array, name, first_sep)
    res = _header(len(list_arrays[0]), first_sep) + mid + _footer()
    if "p" in output:
        print(res)
    if "c" in output:
        copy_to_clipboard(res)
    if "s" in output:
        file_print(res)
    if "r" in output:
        return res