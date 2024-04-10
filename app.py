from flask import Flask, render_template, request, redirect, url_for, jsonify
from datamanager.json_data_manager import JSONDataManager, \
    UserNotFoundException, MovieNotFoundException, MovieExistsException
import os

# Define the path to the data.json file
data_json_path = os.path.join(os.path.dirname(__file__), 'datamanager', 'data.json')

app = Flask(__name__)
data_manager = JSONDataManager(data_json_path)  # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


# Route for displaying user's favorite movies
@app.route('/users/<int:user_id>')
def display_user_movies(user_id):
    try:
        # Fetch user's movies based on user_id
        # movies = fetch_movies(user_id)
        # Render user_movies.html template with movies data
        # return render_template('user_movies.html', movies=movies)
        movies = data_manager.get_user_movies(user_id)
        print(movies)
        # user = data_manager.get_username_by_id(user_id)
        user = data_manager.get_user_info(user_id)
        # Display the movies for the user
        return render_template('user_movies.html', user=user, movies=movies)
    except UserNotFoundException:
        # Redirect the user to a different page
        return redirect(url_for('user_not_found', user_id=user_id))


# Route for displaying form to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username')

        # Check if the username is not empty
        if username:
            # Check if the user with the same name already exists
            existing_user_id = data_manager.get_user_id_by_name(username)
            if existing_user_id is not None:
                # User with the same name already exists
                error_message = f"A user with the name '{username}' already exists."

                # Render the template with the error message
                render_template('add_user.html', error_message=error_message)

            else:
                # Add the new user
                data_manager.add_user(username)

                # Redirect to the users page
                return redirect(url_for('list_users'))

        """# Add the new user
        data_manager.add_user(username)
        # Redirect to the users page
        return redirect(url_for('list_users'))"""

    # If it's a GET request or if there were validation errors, render the add_user.html template
    return render_template('add_user.html', error_message=error_message)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['title']
        try:
            data_manager.add_movie(user_id, title)
            return redirect(f'/users/{user_id}')
        except UserNotFoundException:
            return redirect(f'/user_not_found/{user_id}')
        except (MovieNotFoundException, MovieExistsException) as exception:
            return render_template('error.html', message=str(exception))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/')
def update_movie():
    pass


@app.route('/users/<int:user_id>/delete_movie/<movie_id>', methods=['DELETE'])
def delete_movie(user_id, movie_id):
    try:
        # Delete the movie
        data_manager.delete_movie(user_id, movie_id)
        # return redirect(f'/users/{user_id}')
        return jsonify({'message': f'Movie with id {movie_id} has been deleted successfully.'}), 200
    except UserNotFoundException:
        return redirect(f'/user_not_found/{user_id}')
    except MovieNotFoundException as exception:
        return render_template('error.html', message=str(exception))


@app.route('/user_not_found/<int:user_id>')
def user_not_found(user_id):
    return render_template('error.html', message=f"Sorry, the requested user with ID {user_id} does not exist.")


@app.route('/error')
def error():
    return render_template('error.html', message="An error occurred.")


if __name__ == '__main__':
    app.run(debug=True)
