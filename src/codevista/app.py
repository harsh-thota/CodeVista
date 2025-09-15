from textual.app import App, ComposeResult
from textual.widgets import Footer


class CodeVistaApp(App):
    def compose() -> ComposeResult:
        yield Footer()