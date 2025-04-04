from model import PainelModel
from view import PainelView

class PainelController:
    """Controller for the Painel screen."""
    
    def __init__(self):
        self.model = PainelModel()
    
    def run(self):
        """Run the application."""
        app = PainelView(
            title=self.model.get_title(),
            content=self.model.get_content()
        )
        app.run() 