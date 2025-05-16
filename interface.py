from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Label, TabPane, TabbedContent, MarkdownViewer, Input, Button

class PainelCafeApp(App):
    """Painel do Cafe application."""

    TITLE = "Painel do Cafe"
    # CSS_PATH = "painel_cafe.tcss"
    __promo_markdown: str

    def set_promo_markdown(self, promos: str) -> None:
        self.__promo_markdown = promos

    def __compose_form_compras(self) -> ComposeResult:
        """Create form widgets for the purchases tab."""
        yield Label("Café:")
        yield Input(placeholder="Nome do café")
        yield Label("Quantidade (g):")
        yield Input(placeholder="500")
        yield Label("Preço (R$):")
        yield Input(placeholder="50.00")
        yield Label("Data da compra:")
        yield Input(placeholder="DD/MM/AAAA")
        yield Button("Adicionar compra", variant="primary")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with TabbedContent():
            with TabPane("Promocoes"):
                yield MarkdownViewer(markdown=self.__promo_markdown, show_table_of_contents=True)
            with TabPane("Compras"):
                yield from self.__compose_form_compras()
            with TabPane("Receitas"):
                yield Label("Relatorios")

