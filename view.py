from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static

class PainelView(App):
    """A Textual app for the Painel screen."""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    #content {
        width: 80%;
        height: auto;
        padding: 1;
        border: solid green;
    }
    """
    
    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            Static(self.content, id="content"),
            id="main-container"
        )
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the app when it starts."""
        self.title = self.title 