from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Label, TabPane, TabbedContent, MarkdownViewer, Input, Button, TextArea, Checkbox
from textual.message import Message
import json
from pathlib import Path

class PainelCafeApp(App):
    """Painel do Cafe application."""

    TITLE = "Painel do Cafe"
    # CSS_PATH = "painel_cafe.tcss"
    __promo_markdown: str
    __products_list: dict[str, list[dict]]
    NOTES_FILE = "anotacoes.json"

    def __init__(self):
        super().__init__()
        self.__mock_products_list()


    def set_promo_markdown(self, promos: str) -> None:
        self.__promo_markdown = promos

    def __mock_products_list(self) -> None:
        self.__products_list = {
            "Dutra": [
                {"name": "Café sensações 500g", "price": 10, "description": "descrição café sensações", "quantity": 1, "link": "https://www.google.com"},
                {"name": "Café doçura 500g", "price": 12, "description": "descrição café doçura", "quantity": 1, "link": "https://www.google.com"},
            ],
            "Encantos": [
                {"name": "Café encantos 500g", "price": 15, "description": "descrição café encantos", "quantity": 1, "link": "https://www.google.com"},
                {"name": "Café agrado 500g", "price": 15, "description": "descrição café agrado", "quantity": 1, "link": "https://www.google.com"},
                {"name": "Café raro 500g", "price": 15, "description": "descrição café raro", "quantity": 1, "link": "https://www.google.com"},
            ],
        }

    def __mock_build_interface(self) -> None:
        self.__interface = [
            {"type": "label", "conf": {"text": "Café: Café sensações 600g", "expand": True, "shrink": True, "markup": True, "name": "cafe_sencacoes", "id": "cafe-sensacoes", "classes": None, "disabled": False}, "child": None},
            {"type": "label", "conf": {"text": "Café: Café sensações 500g", "expand": True, "shrink": True, "markup": True, "name": "cafe_sencacoes_2", "id": "cafe-sensacoes-2", "classes": None, "disabled": False}, "child": None}
        ]

    def set_products_list(self, products: dict[str, list[dict]]) -> None:
        self.__products_list = products

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
        
    def __compose_product_form(self, product: dict) -> ComposeResult:
        """Create form widgets for the purchases tab."""
        yield Label(f"Café: {product['name']}")
        yield Label(f"Descrição: {product['description']}")
        yield Label(f"Preço unitário: R$ {product['price']:.2f}")
        yield Label("Quantidade:")
        yield Input(value=str(product["quantity"]))
        yield Label(f"Link: {product['link']}")
   
   
   
   
        yield Checkbox("Comprar")

    def __compose_form_compras(self) -> ComposeResult:
        for store, products in self.__products_list.items():
            yield Label(store)
            for product in products:
                yield from self.__compose_product_form(product)

        yield Button("Gerar lista de compras", variant="primary")

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

