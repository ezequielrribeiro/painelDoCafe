from textual.app import App, ComposeResult
from textual.widgets import Header, Label

class PainelCafeApp(App):
    """Painel do Cafe application."""

    TITLE = "Painel do Cafe"
    CSS_PATH = "painel_cafe.tcss"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label("Bem-vindo ao painel do cafe") 