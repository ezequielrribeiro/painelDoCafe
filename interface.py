from textual.app import App, ComposeResult
from textual.widgets import Header, Label, TabPane, TabbedContent, MarkdownViewer

class PainelCafeApp(App):
    """Painel do Cafe application."""

    TITLE = "Painel do Cafe"
    # CSS_PATH = "painel_cafe.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with TabbedContent():
            with TabPane("Promocoes"):
                yield MarkdownViewer("""
                # Moka Clube
                - 10% de desconto na compra de 2 cafes
                - 20% de desconto na compra de 3 cafes
                - 30% de desconto na compra de 4 cafes
                # Unique Cafes
                - 10% de desconto na compra de 2 cafes
                - 20% de desconto na compra de 3 cafes
                - 30% de desconto na compra de 4 cafes
                # Netcafes
                - 10% de desconto na compra de 2 cafes
                - 20% de desconto na compra de 3 cafes
                - 30% de desconto na compra de 4 cafes
                """, show_table_of_contents=True)
            with TabPane("Compras"):
                yield Label("Configuracoes")
            with TabPane("Receitas"):
                yield Label("Relatorios")

