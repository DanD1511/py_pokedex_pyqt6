from abc import ABC, abstractmethod
import requests


class ApiClient(ABC):
    @abstractmethod
    def get(self, url: str):
        pass


class PokeApiClient(ApiClient):
    def get(self, url: str):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Response code {response.status_code} is not 200")
        except Exception as e:
            raise ConnectionError(f"Error connecting to {url}: {e}")


class PokemonDataFetcher:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def fetch_data(self, pokemon_name: str):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        return self.api_client.get(url)


class Pokemon:
    def __init__(self, name: str, data_fetcher: PokemonDataFetcher):
        self.name = name.lower()
        self.data_fetcher = data_fetcher
        self.pokemon_data = self.data_fetcher.fetch_data(self.name)

    def get_pokemon_abilities(self):
        return [ability['ability']['name'] for ability in self.pokemon_data['abilities']]

    def get_pokemon_types(self):
        return [types['type']['name'] for types in self.pokemon_data['types']]

    def get_pokemon_stats(self):
        if self.pokemon_data:
            print(f"Name: {self.pokemon_data['name'].capitalize()}")
            print(f"Type: {self.get_pokemon_types()}")
            print(f"Ability: {self.get_pokemon_abilities()}")
        else:
            print("This pokemon don't have stats")
