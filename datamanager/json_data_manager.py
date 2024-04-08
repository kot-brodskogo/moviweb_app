import json
import os
from data_manager_interface import DataManagerInterface


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
        Return all users from the JSON file.

        Returns:
             dict: Dictionary of users, where keys are user IDs and values are user data.
        """
        return self.data.get('users', {})

    def get_user_movies(self, user_id):
        """
        Return all the movies for a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: Dictionary of movies for the given user, where keys are movie IDs and values are movie data.
        """
        if not self._user_exists(user_id):
            print(f"user {user_id} not exists")
            return {}

        user_id_str = str(user_id)
        return self.data['users'][user_id_str].get('movies', {})

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

    def add_movie(self, user_id, movie_data):
        """
        Add a movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_data (dict): Dictionary containing movie data to be added.
        """
        if not self._user_exists(user_id):
            print(f"User with ID '{user_id}' does not exist.")
            return

        # Get the user's movies and movie ID
        movies = self.get_user_movies(user_id)
        movie_id = movie_data.get('id')

        if self._movie_exists(user_id, movie_id):
            return

        print(f"Movie with ID '{movie_id}' not found for user '{user_id}'.")
        movies[movie_id] = movie_data

        self._save_data(self.data)

    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie for a given user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to check.
        """

        # Check if the user exists
        if not self._user_exists(user_id):
            print(f"User with ID '{user_id}' does not exist.")
            return

        # Check if the movie exists for the user
        if not self._movie_exists(user_id, movie_id):
            print(f"Movie with ID '{movie_id}' not found for user '{user_id}'.")
            return

        # Get the user's movies
        movies = self.get_user_movies(user_id)

        # Delete the movie from the user's movies
        del movies[movie_id]

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
        # Check if the user exists
        if not self._user_exists(user_id):
            print(f"User with ID '{user_id}' does not exist.")
            return

        # Check if the movie exists for the user
        if not self._movie_exists(user_id, movie_id):
            print(f"Movie with ID '{movie_id}' not found for user '{user_id}'.")
            return

        # Get the user's movies
        movies = self.get_user_movies(user_id)

        # Update the movie data
        movies[str(movie_id)].update(new_movie_data)

        # Save the updated data
        self._save_data(self.data)


# test unit
json_manager = JSONDataManager('data.json')
"""all_users = json_manager.get_all_users()
print("All users:", all_users)
# Extract names of users
user_names = [user['name'] for user in all_users.values()]
print(user_names)"""
# user_movies = json_manager.get_user_movies(1)
# print(f"Movies of user {1}:", user_movies)
json_manager.add_movie(1, {'id': 10, 'title': 'Movie 10'})
json_manager.add_movie(2, {'id': 29, 'title': 'Movie 29'})
json_manager.add_movie(1, {'id': 29, 'title': 'Movie 29'})
print("All movies:")
print(json_manager.list_movies())

data_manager = JSONDataManager('test_data.json')
"""all_users_test = data_manager.get_all_users()
print("All users:", all_users_test)
# Extract names of users
user_names_test = [user['name'] for user in all_users_test.values()]
print(user_names_test)"""
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
"""all_users_test_test = test_manager.get_all_users()
print("All users:", all_users_test_test)"""
user_movies = test_manager.get_user_movies(3)
print(f"Movies of user {3}:", user_movies)
test_manager.add_movie(1, {'id': 1, 'title': 'Movie 1'})
test_manager.add_movie(1, {'id': 2, 'title': 'Movie 2'})
print("All movies:")
print(test_manager.list_movies())
