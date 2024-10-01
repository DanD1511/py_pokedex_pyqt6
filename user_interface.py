from io import BytesIO

import requests
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget

from api_client import PokeApiClient


class Pokedex(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokedex")
        self.setGeometry(100, 100, 300, 400)
        self.ui_init()  # Iniciamos la interfaz en el constructor

    def ui_init(self):
        layout = QVBoxLayout()

        self.label_name = QLabel("Enter the pokemon name: ")
        self.input_name = QLineEdit()

        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)

        self.search_button = QPushButton("Search pokemon")
        self.search_button.clicked.connect(self.search_pokemon)
        layout.addWidget(self.search_button)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        self.label_stats = QLabel()
        self.label_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_stats)

        self.setLayout(layout)

    def search_pokemon(self):
        pokemon_name = self.input_name.text().lower()
        api_client = PokeApiClient()
        try:
            data = api_client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
            self.show_pokemon(data)  # Llamar a la función para mostrar el Pokémon
        except Exception as e:
            self.label_stats.setText(f"Error: {str(e)}")
            self.image_label.clear()

    def show_pokemon(self, data):
        pokemon_img_url = data['sprites']['front_default']
        if pokemon_img_url:
            response = requests.get(pokemon_img_url)
            pokemon_img = Image.open(BytesIO(response.content))
            pokemon_img = pokemon_img.convert("RGBA")

            pokemon_ui_image = QPixmap()
            pokemon_ui_image.loadFromData(BytesIO(response.content).getvalue())

            self.image_label.setPixmap(pokemon_ui_image.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

        # Mostrar estadísticas del Pokémon
        nombre = data['name'].capitalize()
        tipos = ', '.join([tipo['type']['name'] for tipo in data['types']])
        habilidades = ', '.join([habilidad['ability']['name'] for habilidad in data['abilities']])

        stats_text = f"Name: {nombre}\nTypes: {tipos}\nAbilities: {habilidades}"
        self.label_stats.setText(stats_text)
