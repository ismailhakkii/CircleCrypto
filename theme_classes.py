# theme_classes.py
from typing import Dict

class EncryptionTheme:
    def __init__(self, name: str, colors: Dict[str, str]):
        self.name = name
        self.colors = colors