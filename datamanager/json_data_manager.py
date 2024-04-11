from .data_manager_interface import DataManagerInterface
from .data_exceptions import UserNotFoundException, MovieNotFoundException, MovieExistsException
from .movie_api import MovieAPI
import json
import os


class JSONDataManager(DataManagerInterface):
    def __init__(self, filepath):
        """
        Initialize the JSONDataManager.

        Args:
             filepath (str): The path to the JSON file.
        """
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            self._create_default_json_file()
            # print(f"Storage file '{self.filepath}' created successfully.")
        self.data = self._load_data()  # Load the data during initialization

    def _create_default_json_file(self):
        """Create a JSON file with default user if it does not exist."""
        default_data = {
            "users": {
                "0": {
                    "id": 0,
                    "name": "Default User",
                    "movies": {}
                }
            }
        }

        self._save_data(default_data)
        # print(f"Default user data saved to file '{self.filepath}'.")

    def _load_data(self):
        """
        Load data from the JSON file.

        Returns:
            dict: Data loaded from the JSON file, or an empty dictionary if the file is empty.
        """
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data from file '{self.filepath}': {e}")
            data = {}
        return data

    def _save_data(self, data):
        """
        Save data to the JSON file.

        Args:
            data (dict): The data to be saved to the file.
        """
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data to file '{self.filepath}': {e}")

    def get_all_users(self):
        """
        Return all users from the JSON file with only their IDs and names.

        Returns:
            dict: Dictionary of users, where keys are user IDs and values are user data containing only ID and name.
        """
        return {user_id: {'id': user_info['id'], 'name': user_info['name']} for user_id, user_info
                in self.data.get('users', {}).items()}

    def get_user_movies(self, user_id):
        """
        Return all the movies for a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: Dictionary of movies for the given user, where keys are movie IDs and values are movie data.

        Raises:
            UserNotFoundException: If the requested user is not found.
        """
        user_id_str = str(user_id)

        if user_id_str not in self.data['users']:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        return self.data['users'][user_id_str].get('movies', {})

    def get_movie(self, user_id, movie_id):
        """
        Get details of a specific movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_id (str): The ID of the movie.

        Returns:
            dict: Dictionary containing movie details if found.

        Raises:
            MovieNotFoundException: If the movie is not found for the given user.
        """
        user_movies = self.get_user_movies(user_id)

        # Check if the movie exists for the user
        if movie_id in user_movies:
            return user_movies[movie_id]
        else:
            raise MovieNotFoundException(f"Movie with ID {movie_id} not found for user {user_id}.")

    def get_user_info(self, identifier):
        """
        Get user information by user ID or username.

        Args:
            identifier (int or str): The ID or name of the user.

        Returns:
            dict or None: The user information if found, otherwise None.
        """
        if isinstance(identifier, int):
            return self.data['users'].get(str(identifier))
        elif isinstance(identifier, str):
            for user_data in self.data['users'].values():
                if user_data['name'] == identifier:
                    return user_data
        return None

    def list_movies(self):
        """
        Lists all movies stored in the JSON file.

        Returns:
            dict: A dictionary containing movie titles as keys and movie information as values.
        """
        all_movies = {}

        for user_data in self.data['users'].values():
            movies = user_data.get('movies', {})
            all_movies.update(movies)

        return all_movies

    def add_movie(self, user_id, title):
        """
        Add a movie to the user's collection.

        Args:
            user_id (int): The ID of the user.
            title (str): The title of the movie to be added.

        Raises:
            UserNotFoundException: If the user with the specified user_id is not found.
            MovieNotFoundException: If the movie with the specified title is not found in the OMDB database.
            MovieExistsException: If the movie already exists in the user's collection.

        Returns:
            None
        """
        # Step 1: Find the user
        if str(user_id) not in self.data['users']:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        user_movies = self.get_user_movies(user_id)

        # Step 2: Fetch information about the movie from the OMDB API
        movie_info = MovieAPI.fetch_movie_info(title)
        if movie_info.get('Response') == 'False':
            # Movie not found in the OMDB database
            raise MovieNotFoundException(f"Movie '{title}' not found.")

        # Step 3: Add the movie to the user's movie collection
        movie_id = movie_info.get('imdbID')
        if movie_id in user_movies:
            raise MovieExistsException(f"Movie '{title}' already exists in user's collection.")

        user_movies[movie_id] = {
            'id': movie_id,
            'title': movie_info.get('Title'),
            'director': movie_info.get('Director'),
            'year': int(movie_info.get('Year')),
            'rating': float(movie_info.get('imdbRating')),
            'poster_url': movie_info.get('Poster', '')
        }

        # Save the updated data to the file
        self._save_data(self.data)

    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to check.

        Raises:
            MovieNotFoundException: If the movie with the specified title is not found.

        Returns:
            None
        """
        # Step 1: Retrieve the user's movies using get_user_movies
        user_movies = self.get_user_movies(user_id)

        # Step 2: Check if the movie exists for the user
        if str(movie_id) not in user_movies:
            raise MovieNotFoundException(f"Movie with ID {movie_id} not found for user {user_id}.")

        # Step 3: Delete the movie from the user's movies
        del user_movies[str(movie_id)]

        # Save the updated data to the file
        self._save_data(self.data)

    def update_movie(self, user_id, movie_id, new_movie_data):
        """
        Update a movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be updated.
            new_movie_data (dict): Dictionary containing updated movie data.

        Raises:
            MovieNotFoundException: If the movie with the specified title is not found.

        Returns:
            None
        """
        # Get the user's movies
        user_movies = self.get_user_movies(user_id)

        # Check if the movie exists for the user
        if str(movie_id) not in user_movies:
            raise MovieNotFoundException(f"Movie with ID {movie_id} not found for user {user_id}.")

        # Update the movie data
        user_movies[str(movie_id)].update(new_movie_data)

        # Save the updated data
        self._save_data(self.data)

    def generate_unique_user_id(self):
        """
        Generate a unique user ID based on existing IDs in the data.

        Returns:
            int: A unique user ID.
        """
        # Get the existing user IDs
        existing_ids = [int(user_id) for user_id in self.data['users']]

        # Generate a unique user ID
        if existing_ids:
            new_id = max(existing_ids) + 1
        else:
            # If no existing user, start from 1
            new_id = 1

        return new_id

    def add_user(self, user_name):
        """
        Add a new user with a generated user ID.

        Args:
            user_name (str): The name of the user to be added.

        Returns:
            None
        """
        generated_id = self.generate_unique_user_id()

        # Create a new user entry
        new_user_data = {
            "id": generated_id,
            "name": user_name,
            "movies": {}
        }

        # Add the new user to the data dictionary
        self.data['users'][str(generated_id)] = new_user_data

        # Save the updated data
        self._save_data(self.data)

    def update_user(self, user_id, new_user_name):
        """
        Update user's name.

        Args:
            user_id (int): The ID of the user to be updated.
            new_user_name (str): The new name for the user.

        Raises:
            UserNotFoundException: If the user with the specified user_id is not found.

        Returns:
            None
        """
        user_id_str = str(user_id)

        # Check if the user exists
        if user_id_str not in self.data['users']:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        # Update the user's name
        self.data['users'][user_id_str]['name'] = new_user_name

        # Save the updated data
        self._save_data(self.data)

    def delete_user(self, user_id):
        """
        Delete a user and associated data.

        Args:
            user_id (int): The ID of the user to be deleted.

        Raises:
            UserNotFoundException: If the user with the specified user_id is not found.

        Returns:
            None
        """
        user_id_str = str(user_id)

        # Check if the user exists
        if user_id_str not in self.data['users']:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        # Remove the user entry
        del self.data['users'][user_id_str]

        # Save the updated data
        self._save_data(self.data)
