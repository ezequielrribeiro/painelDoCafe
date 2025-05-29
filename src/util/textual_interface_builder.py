# build a textual interface from information in a dictionary

from textual.widgets import Widget, Label, Input, Button, Checkbox, TextArea, MarkdownViewer
from textual.containers import Vertical, Horizontal
from typing import Any, Dict, List, Optional, Type

class TextualInterfaceBuilder:
    """Builds Textual interface components from dictionary configurations."""

    __WIDGET_MAPPING = {
        "label": Label,
        "input": Input,
        "button": Button,
        "checkbox": Checkbox,
        "textarea": TextArea,
        "markdown": MarkdownViewer,
        "vertical": Vertical,
        "horizontal": Horizontal
    }

    def __init__(self):
        self._widgets: List[Widget] = []

    def build_widget_from_dict(self, config: Dict[str, Any]) -> Widget:
        """Build a widget from a configuration dictionary.
        
        Args:
            config: Dictionary containing widget configuration
                {
                    "type": str,  # Widget type (label, input, button, etc)
                    "conf": dict, # Widget configuration (text, id, classes, etc)
                    "child": Optional[dict] # Child widget configuration
                }
        
        Returns:
            Widget: The constructed Textual widget
        """
        widget_type = config.get("type", "").lower()
        if widget_type not in self.__WIDGET_MAPPING:
            raise ValueError(f"Unknown widget type: {widget_type}")

        widget_class = self.__WIDGET_MAPPING[widget_type]
        widget_conf = config.get("conf", {})
        
        # Create the widget
        return widget_class(**widget_conf)

    def build_widget_from_html(self, html: str) -> Widget:
        """Build a widget from a html item.
        
        Args:
            config: html component
        
        Returns:
            Widget: The constructed Textual widget
        """

        # TODO: make html interpreter to dict, then build_widget_from_dict is called

