import os
from collections import OrderedDict
from thefuzz import process
from functools import cache


@cache
def read_history():
    path = os.path.expanduser("~/.zsh_history")
    with open(path, "rb") as file:
        bytes = file.read()
    text = bytes.decode("utf-8", "ignore")
    lines = text.split("\n")
    commands = [line.rsplit(";", 1)[-1] for line in lines if line.strip()]
    unique_list = list(OrderedDict.fromkeys(commands))
    unique_list.reverse()
    return unique_list


history = read_history()


fuzzy_history = process.extract("git clone", history, limit=50)
unique_list = list(OrderedDict.fromkeys(fuzzy_history))
# tuple_history = [(line,) for line, score in unique_list if score >= 80]
