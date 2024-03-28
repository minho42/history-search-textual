from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Input, DataTable
import os
from collections import OrderedDict
from functools import cache, wraps
import threading


def debounce(seconds):
    def decorator(func):
        @wraps(func)
        def debounced(*args, **kwargs):
            def call_it():
                func(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = threading.Timer(seconds, call_it)
            debounced.t.start()

        return debounced

    return decorator


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
    result = [(line,) for line in history if query.lower() in line.lower()]
    return result


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

    @debounce(0.3)
    def on_input_changed(self, message):
        table = self.query_one(DataTable)
        table.clear()
        result = search_result(message.value)
        table.add_rows(result)


if __name__ == "__main__":
    app = HistorySearchApp()
    app.run()
