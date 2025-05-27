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

    def build_from_dict(self, config: Dict[str, Any]) -> Widget:
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

    def build_from_list(self, configs: List[Dict[str, Any]]) -> List[Widget]:
        """Build multiple widgets from a list of configurations.
        
        Args:
            configs: List of widget configuration dictionaries
            
        Returns:
            List[Widget]: List of constructed Textual widgets
        """
        return [self.build_from_dict(config) for config in configs]

    def build_container(self, container_type: str, widgets: List[Dict[str, Any]]) -> Widget:
        """Build a container widget with multiple child widgets.
        
        Args:
            container_type: Type of container ("vertical" or "horizontal")
            widgets: List of widget configurations to be added to the container
            
        Returns:
            Widget: The container widget with mounted children
        """
        if container_type not in ["vertical", "horizontal"]:
            raise ValueError("Container type must be 'vertical' or 'horizontal'")
            
        container_class = self.__WIDGET_MAPPING[container_type]
        container = container_class()
        
        for widget_config in widgets:
            widget = self.build_from_dict(widget_config)
            container.mount(widget)
            
        return container
