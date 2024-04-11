// Add an event listener to all elements with the class "delete-movie"
document.querySelectorAll('.delete-movie').forEach(link => {
    link.addEventListener('click', function(event) {
        // Prevent the default behavior of the link
        event.preventDefault();

        // Retrieve the user ID and movie ID from the data attributes
        const userId = this.dataset.user;
        const movieId = this.dataset.movie;

        // Display the confirmation modal
        const modal = document.getElementById('myModal');
        modal.style.display = 'block';

        // Add event listener to the "Yes, Delete" button in the modal
        document.getElementById('confirmDelete').addEventListener('click', function() {
            // Send a DELETE request to the server
            fetch(`/users/${userId}/delete_movie/${movieId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete movie');
                }
                // Redirect to the user_movies page upon successful deletion
                window.location.href = `/users/${userId}`;
            })
            .catch(error => {
                console.error('Error deleting movie:', error);
                // Handle the error (e.g., display an error message to the user)
            });
        });

        // Add event listeners for the "Cancel" button and the close button in the modal
        document.getElementById('cancelDelete').addEventListener('click', closeModal);
        document.querySelector('.close').addEventListener('click', closeModal);

        // Function to close the modal
        function closeModal() {
            // Close the modal
            const modal = document.getElementById('myModal');
            modal.style.display = 'none';
        }
    });
});
