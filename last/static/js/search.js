function search() {
    var searchCategory = document.getElementById('search_category').value;
    var searchTerm = document.getElementById('search_term').value;
    
    fetch('/students', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `search_category=${searchCategory}&search_term=${searchTerm}`
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('searchResults', JSON.stringify(data)); // 検索結果をセッションストレージに保存
        window.location.href = '../templates/result.html'; // result.htmlへリダイレクト
        
        });
}
