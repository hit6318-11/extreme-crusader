new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
        invalid: false
    },
    methods: {
        search() {
            var searchCategory = document.getElementById('search_category').value;
            var searchTerm = document.getElementById('search_term').value;
            var url = `/api/students?${encodeURIComponent(searchCategory)}=${encodeURIComponent(searchTerm)}`;
            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                this.invalid = false;
                const oldResults = sessionStorage.getItem('searchResults');
                if (oldResults){
                    sessionStorage.removeItem('searchResults');
                }
                sessionStorage.setItem('searchResults', JSON.stringify(data));
                window.location.href = '/result';
            })
            .catch(error => {
                this.invalid = true;
                console.error('Error fetching data:', error);
            });
        },
        register() {
            window.location.href = '/form';
        },
        logout() {
            window.location.href = '/logout';
    }
}
});
