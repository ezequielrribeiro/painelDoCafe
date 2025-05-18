from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Label, TabPane, TabbedContent, MarkdownViewer, Input, Button, TextArea
from textual.message import Message
import json
from pathlib import Path

class PainelCafeApp(App):
    """Painel do Cafe application."""

    TITLE = "Painel do Cafe"
    # CSS_PATH = "painel_cafe.tcss"
    __promo_markdown: str
    NOTES_FILE = "anotacoes.json"

    def set_promo_markdown(self, promos: str) -> None:
        self.__promo_markdown = promos

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "save_notes":
            textarea = self.query_one("#anotacoes_textarea", TextArea)
            notes = textarea.text
            self.save_notes(notes)

    def save_notes(self, notes: str) -> None:
        """Save notes to a JSON file."""
        data = {"notes": notes}
        with open(self.NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_notes(self) -> str:
        """Load notes from the JSON file."""
        try:
            with open(self.NOTES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("notes", "")
        except FileNotFoundError:
            return ""

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

    def __compose_form_anotacoes(self) -> ComposeResult:
        """Create form widgets for the notes tab."""
        with Vertical():
            yield Label("Anotações:")
            yield TextArea(tooltip="Digite suas anotações aqui...", id="anotacoes_textarea")
            yield Button("Salvar", variant="primary", id="save_notes")


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with TabbedContent():
            with TabPane("Promocoes"):
                yield MarkdownViewer(markdown=self.__promo_markdown, show_table_of_contents=True, open_links=False)
            with TabPane("Compras"):
                yield from self.__compose_form_compras()
            with TabPane("Anotações"):
                yield from self.__compose_form_anotacoes()

    def on_mount(self) -> None:
        """Load saved notes when the app starts."""
        textarea = self.query_one("#anotacoes_textarea", TextArea)
        textarea.text = self.load_notes()

