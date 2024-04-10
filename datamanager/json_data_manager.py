from .data_manager_interface import DataManagerInterface
from .movie_api import MovieAPI
import json
import os


class UserNotFoundException(Exception):
    """Exception raised when the requested user is not found."""
    pass


class MovieNotFoundException(Exception):
    """Exception raised when the requested movie is not found."""
    pass


class MovieExistsException(Exception):
    """Exception raised when the requested movie is already exists."""
    pass


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
            print(f"Storage file '{self.filepath}' created successfully.")
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

        self._save_data(default_data)  # Use the _save_data method to save the default data
        print(f"Default user data saved to file '{self.filepath}'.")

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
        # Get the user's movies
        user_movies = self.get_user_movies(user_id)

        # Check if the movie exists for the user
        if movie_id in user_movies:
            return user_movies[movie_id]
        else:
            raise MovieNotFoundException(f"Movie with ID {movie_id} not found for user {user_id}.")

    def _user_exists(self, user_id):
        """
        Check if a user with the given ID exists in the loaded data.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user_id_str = str(user_id)
        return user_id_str in self.data['users']

    def _movie_exists(self, user_id, movie_id):
        """
        Check if a movie exists for the given user.

        Args:
            user_id (int): The ID of the user to check.
            movie_id (int): The ID of the movie to check.

        Returns:
            bool: True if the movie exists, False otherwise.
        """
        user_id_str = str(user_id)
        movie_id_str = str(movie_id)
        print("WE ARE HERE")
        print(f"user is str {user_id_str} movie id {movie_id_str}")
        print(f"{self.data['users'][user_id_str].get('movies')}")

        # Get the dictionary of movies for the user (or an empty dictionary if no movies exist)
        movies_dict = self.data['users'].get(user_id_str, {}).get('movies', {})
        print(movies_dict)
        print(f"answer is {movie_id_str in movies_dict}")
        # Check if the movie_id exists as a key in the movies_dict
        return movie_id_str in movies_dict

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

    def add_movie(self, user_id, title):
        # Step 1: Find the user
        if str(user_id) not in self.data['users']:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        user_movies = self.get_user_movies(user_id)  # Use get_user_movies here

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
        print(f"Movie '{title}' added to user {user_id}'s collection.")

    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to check.
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

        print(f"Movie with ID {movie_id} deleted for user {user_id}.")

        # Save the updated data
        self._save_data(self.data)

    def update_movie(self, user_id, movie_id, new_movie_data):
        """
        Update a movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be updated.
            new_movie_data (dict): Dictionary containing updated movie data.
        """
        # Get the user's movies
        user_movies = self.get_user_movies(user_id)

        print(f"I've been here and those are {user_movies}")

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

    def get_username_by_id(self, user_id):
        """
        Get username by user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            str: The name of the user with the given ID, or None if the user is not found.
        """
        return self.data['users'].get(str(user_id), {}).get('name')

    def get_user_id_by_name(self, user_name):
        """
        Get the user ID by the username.

        Args:
            user_name (str): The name of the user.

        Returns:
            int or None: The user ID if found, otherwise None.
        """
        for user_id, user_data in self.data['users'].items():
            if user_data['name'] == user_name:
                return int(user_id)
        return None

    def add_user(self, user_name):
        """
        Add a new user. user_id should be generated.

        Args:
            user_name (str): The name of the user to be added.

        Returns:
            int: The generated user ID.
        """
        # Check if a user with the same name already exists
        """existing_user_id = self.get_user_id_by_name(user_name)
        if existing_user_id is not None:
            # User with the same name already exists
            print(f"A user with the name '{user_name}' already exists.")

            # Ask the user if they want to create a new user or stick with the existing one
            choice = input("Do you want to create a new user? (yes/no): ").lower()
            if choice != "yes":
                # Stick with the existing user
                return existing_user_id"""

        # Generate a unique user ID
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
        """
        user_id_str = str(user_id)

        # Check if the user exists
        if not self._user_exists(user_id):
            print(f"User with ID '{user_id}' does not exist.")
            return

        # Update the user's name
        self.data['users'][user_id_str]['name'] = new_user_name

        # Save the updated data
        self._save_data(self.data)

    def delete_user(self, user_id):
        """
        Delete a user and associated data.

        Args:
            user_id (int): The ID of the user to be deleted.
        """
        user_id_str = str(user_id)

        # Check if the user exists
        if not self._user_exists(user_id):
            print(f"User with ID '{user_id}' does not exist.")
            return

        # Remove the user entry
        del self.data['users'][user_id_str]

        # Save the updated data
        self._save_data(self.data)


# test unit
"""json_manager = JSONDataManager('data.json')
all_users = json_manager.get_all_users()
print("All users:", all_users)
# Extract names of users
user_names = [user['name'] for user in all_users.values()]
print(user_names)
# user_movies = json_manager.get_user_movies(1)
# print(f"Movies of user {1}:", user_movies)
json_manager.add_movie(1, {'id': 10, 'title': 'Movie 10'})
json_manager.add_movie(2, {'id': 29, 'title': 'Movie 29'})
json_manager.add_movie(1, {'id': 29, 'title': 'Movie 29'})
print("All movies:")
print(json_manager.list_movies())

data_manager = JSONDataManager('test_data.json')
all_users_test = data_manager.get_all_users()
print("All users:", all_users_test)
# Extract names of users
user_names_test = [user['name'] for user in all_users_test.values()]
print(user_names_test)
# user_movies = data_manager.get_user_movies(2)
# print(f"Movies of user {2}:", user_movies)
# user_movies = data_manager.get_user_movies(5)
# print(f"Movies of user {5}:", user_movies)
data_manager.add_movie(1, {'id': 18, 'title': 'Movie 18'})
data_manager.add_movie(1, {'id': 28, 'title': 'Movie 28'})
print("All movies:")
print(data_manager.list_movies())
print("\nDeleting movie with ID '2' for user 1:")
data_manager.delete_movie(1, 2)
print(data_manager.get_user_movies(1))

# Test updating a movie
print("\nUpdating movie with ID '1' for user 1:")
data_manager.update_movie(1, 1, {'title': 'Updated Movie 1'})
print(data_manager.get_user_movies(1))

test_manager = JSONDataManager('test_test.json')
all_users_test_test = test_manager.get_all_users()
print("All users:", all_users_test_test)
user_movies = test_manager.get_user_movies(3)
print(f"Movies of user {3}:", user_movies)
test_manager.add_movie(1, {'id': 1, 'title': 'Movie 1'})
test_manager.add_movie(1, {'id': 2, 'title': 'Movie 2'})
print("All movies:")
print(test_manager.list_movies())

test_manager.add_user('Stacy')
data_manager.add_user('Stacy')
json_manager.add_user('Stacy')
test_manager.update_user(1, 'Colin')
test_manager.delete_user(1)"""
