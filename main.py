from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Input, DataTable
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
    commands = [line.rsplit(";", 1)[-1].strip() for line in lines if line.strip()]
    unique_list = list(OrderedDict.fromkeys(commands))
    unique_list.reverse()
    return unique_list


history = read_history()


@cache
def search_result(query):
    if not query:
        return []

    fuzzy_history = process.extract(query, history, limit=50)
    unique_list = list(OrderedDict.fromkeys(fuzzy_history))
    tuple_history = [(line,) for line, score in unique_list if score >= 80]
    return tuple_history


class HistorySearchApp(App):
    BINDINGS = [
        Binding("ctrl+c", "app.quit", "Quit", show=True),
    ]
    current_sorts: set = set()

    def compose(self):
        yield Header()
        yield Input(placeholder="search", type="text")
        yield DataTable()
        yield Footer()

    def on_mount(self):
        pass
        table = self.query_one(DataTable)
        table.add_columns(("header",))
        table.show_header = False

    def update_cell(self):
        pass

    def action_toggle_dark(self):
        self.dark = not self.dark

    def on_input_changed(self, message):
        table = self.query_one(DataTable)
        table.clear()
        result = search_result(message.value)
        table.add_rows(result)


if __name__ == "__main__":
    app = HistorySearchApp()
    app.run()
