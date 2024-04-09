import requests


class MovieAPI:
    OMDB_API_KEY = '4b3bad41'

    @staticmethod
    def fetch_movie_info(title):
        """Fetches movie information from the OMDb API."""
        url = f'http://www.omdbapi.com/?apikey={MovieAPI.OMDB_API_KEY}&t={title}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch movie information. Status code: {response.status_code}")
