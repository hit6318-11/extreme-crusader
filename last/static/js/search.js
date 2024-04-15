function search() {
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
        sessionStorage.setItem('searchResults', JSON.stringify(data));
        window.location.href = '/result';
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}