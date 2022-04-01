import os


def kwarg_parser(pairs, **kwargs):
    keys = kwargs.keys()
    for label, default in pairs.items():
        if label in keys:
            yield kwargs.pop(label)
        else:
            yield default


def clear():
    os.system("clear")
