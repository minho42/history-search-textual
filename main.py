import asyncio
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Input, Label, DataTable
import os
from collections import OrderedDict
from thefuzz import fuzz, process
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


@cache
def get_table_data():
    history = read_history()
    tuple_history = [(line,) for line in history]
    return tuple_history


# history = read_history()
# tuple_history = [(line,) for line in history]
# first_row = ("command",)
# tuple_history.insert(0, first_row)
# ROWS = tuple_history


class HistorySearchApp(App):
    BINDINGS = [
        ("d", "toggle_dark", "toggle dark mode"),
        Binding("ctrl+c", "app.quit", "Quit", show=True),
    ]
    current_sorts: set = set()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Search zsh history (reverse-i-search improved) ")
        yield Input(placeholder="search", type="text")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        data = get_table_data()
        first_row = ("command",)
        table.add_columns(first_row)
        table.add_rows(data)
        table.show_header = False

    def update_cell(self):
        pass

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def on_input_changed(self, message) -> None:
        table = self.query_one(DataTable)
        if message.value:
            history = read_history()
            fuzzy_history = process.extract(message.value, history, scorer=fuzz.ratio)
            tuple_history = [(line,) for line, score in fuzzy_history]
            table.clear()
            table.add_rows(tuple_history)
        else:
            table.clear()
            data = get_table_data()
            table.add_rows(data)


if __name__ == "__main__":
    app = HistorySearchApp()
    app.run()
