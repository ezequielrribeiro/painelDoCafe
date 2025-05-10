from textual.app import App, ComposeResult
from textual.widgets import Header, Label, TabPane, TabbedContent, MarkdownViewer

class PainelCafeApp(App):
    """Painel do Cafe application."""

    TITLE = "Painel do Cafe"
    # CSS_PATH = "painel_cafe.tcss"
    __promo_markdown: str

    def setPromoMarkdown(self, promos: str) -> None:
        self.__promo_markdown = promos

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with TabbedContent():
            with TabPane("Promocoes"):
                yield MarkdownViewer(markdown=self.__promo_markdown, show_table_of_contents=True)
            with TabPane("Compras"):
                yield Label("Configuracoes")
            with TabPane("Receitas"):
                yield Label("Relatorios")

