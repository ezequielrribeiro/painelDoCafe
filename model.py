class PainelModel:
    """Model for the Painel screen."""
    
    def __init__(self):
        self.title = "Painel do Cafe"
        self.content = "Bem-vindo ao Painel do Cafe!"
    
    def get_title(self):
        """Get the title of the painel."""
        return self.title
    
    def get_content(self):
        """Get the content of the painel."""
        return self.content 