new Vue({
    el: '#app',
    data: {
        credentials: {
            username: '',
            password: ''
        },
        loginError: false,
        errorMessage: 'Invalid username or password'
    },
    methods: {
        login: function() {
            // Construct the form data to be sent to the server-side route
            const formData = new FormData();
            formData.append('username', this.credentials.username);
            formData.append('password', this.credentials.password);

            // Send a POST request to the server-side route for authentication
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // Redirect to the search page upon successful login
                    window.location.href = '/search';
                } else {
                    // Handle authentication failure
                    this.loginError = true;
                }
            })
            .catch(error => {
                console.error('Error occurred during login:', error);
            });
        },
        register: function() {
            // Redirect to the user registration page
            window.location.href = '/register';
        }
    }
});