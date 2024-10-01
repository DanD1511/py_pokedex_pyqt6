import sys
from PyQt6.QtWidgets import QApplication
from api_client import PokeApiClient
from user_interface import Pokedex

api_client = PokeApiClient()
app = QApplication(sys.argv)
window = Pokedex()
window.show()
sys.exit(app.exec())
