function search() {
    var searchCategory = document.getElementById('search_category').value;
    var searchTerm = document.getElementById('search_term').value;
    
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `search_category=${searchCategory}&search_term=${searchTerm}`
    })
    .then(response => response.json())
    .then(data => {
        var resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        data.forEach(item => {
            resultsDiv.innerHTML += `<p>${JSON.stringify(item)}</p>`;
        });
    });
}
