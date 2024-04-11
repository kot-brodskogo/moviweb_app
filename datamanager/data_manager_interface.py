from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """
        Return all users from the JSON file with only their IDs and names.

        Returns:
            dict: Dictionary of users, where keys are user IDs and values are user data containing only ID and name.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_user_info(self, identifier):
        """
        Get user information by user ID or username.

        Args:
            identifier (int or str): The ID or name of the user.

        Returns:
            dict or None: The user information if found, otherwise None.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def add_user(self, user_name):
        """
        Add a new user with a generated user ID.

        Args:
            user_name (str): The name of the user to be added.

        Returns:
            None
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
