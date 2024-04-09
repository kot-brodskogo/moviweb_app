// Function to handle the click event of delete links
function handleDeleteClick(event) {
    event.preventDefault();

    // Get the user ID and movie ID from the data attributes
    const userId = this.getAttribute('data-user');
    const movieId = this.getAttribute('data-movie');

    // Send a DELETE request to the server
    fetch(`/users/${userId}/delete_movie/${movieId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            // If the deletion was successful, redirect to the user's movies page
            window.location.href = `/users/${userId}`;
        } else {
            // If there was an error, display an alert message
            alert('Failed to delete the movie. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}

// Get all delete links with the 'delete-movie' class
const deleteLinks = document.querySelectorAll('.delete-movie');

// Loop through each delete link
deleteLinks.forEach(link => {
    // Add a click event listener to each link
    link.addEventListener('click', handleDeleteClick);
});