# MovieWeb App 🎥🌐

This application builds upon the foundation of the [Movie App](https://github.com/kot-brodskogo/movieApp), enhancing it with web capabilities powered by Flask and user-specific functionalities.

## Description

The Movie App is a simple command-line application that allows users to manage a collection of movies. Users can add, delete, update, and list movies, as well as perform various operations such as sorting by rating, generating statistics, and creating a movie website.

Now, with the MovieWeb App, these features are accessible through a web interface, making it more convenient for users to interact with their movie collection from anywhere.

## Features

* 🌐 Web Interface: Access your movie collection from any device with a web browser.
* 👤 User-Specific Functionalities: Each user can manage their own personalized movie collection.
* 📊 OMDB API Integration: Fetch additional data about movies from OMDB API to enrich your collection.
* 🖊️ Edit Movie Details: Users can edit the details of movies in their collection, such as title, director, year, and rating.
* 🗑 Delete Movies: Users can remove movies from their collection. ️

## Future ideas
- [ ] When updating a movie info, update poster also 🔄
- [ ] SQLite: A lightweight relational database management system 📊
- [ ] Add user authentication and authorization for secure access 🔐
- [ ] Implement a search and sort functionality 🔍
- [ ] Allow users to write reviews on movies 💬
- [ ] Integrate a recommendation system based on user preferences 🎬
- [ ] Implement a user rating system for movies to allow users to share their own ratings alongside the existing ones from OMDB. ⭐

## Installation
1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd movie-app`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the Flask application: `python app.py`
5. Access the application in your web browser at `http://localhost:5000`

## Usage
* Access the homepage to get started.
* Navigate to the "Users" page to view all users.
* Use the "Add User" page to create a new user.
* View a user's favorite movies by clicking on their name.
* Add a new movie to a user's collection by providing the title.
* Update movie details by clicking on the "Edit" button next to a movie.
* Delete a movie from a user's collection by clicking on the "Delete" button.

### Endpoints

📬 GET /: Display the homepage.

📄 GET /users: Retrieve all users.

📝 POST /add_user: Add a new user.

🔍 GET /users/<user_id>: Display a user's favorite movies.

📝 POST /users/<user_id>/add_movie: Add a new movie to a user's collection.

✏️ GET /users/<user_id>/update_movie/<movie_id>: Update details of a specific movie in a user's collection.

❌ DELETE /users/<user_id>/delete_movie/<movie_id>: Delete a movie from a user's collection.

🔍 GET /user_not_found/<user_id>: Display an error message for a user not found.

❌ GET /error: Display a generic error message.

## Technologies Used
This project utilizes the following technologies:

- Flask: A lightweight web framework for Python 🐍
- HTML: For structuring the web pages 🌐
- CSS: For styling the web pages 🎨
- JavaScript: For dynamic client-side interactions 🚀
- JSON: For storing data in a lightweight, human-readable format 🗃️

## Acknowledgements
This project was created as an exercise to gain hands-on experience with important **Flask** concepts such as routing, template rendering, form handling, and basic CRUD operations. Special thanks to the Flask community for their excellent documentation and resources. 🙌

The Open Movie Database (**OMDb**) API provided crucial functionality for fetching movie information. Its extensive database allowed users to search for movies by title and retrieve detailed information about each film. The project heavily relied on the OMDb API for fetching movie information. 🎬🍿