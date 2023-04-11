from subprocess import run
import numpy as np

def copy_to_clipboard(x):
    run(["xclip", "-selection", "clipboard"], universal_newlines=True, input=x)

def file_print(string, filename="out"):
    with open(filename, "w") as file:
        file.write(string)

def transpose(dump):
    return list(map(list, zip(*dump)))

def load(filename="data", transpose=True):
    with open(filename, "r") as data:
        dump = []
        for line in data.readlines():
            if len(line) and line[0] != '#':
                dump.append(line)
        dump = np.array([[float(x) for x in line.split()] for line in dump])
    if transpose:
        dump = dump.transpose()
    return dump
