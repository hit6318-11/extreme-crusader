new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
        invalid: false // 無効な検索フラグ
    },
    methods: {
        search() {
            var searchCategory = document.getElementById('search_category').value; // 検索カテゴリの取得
            var searchTerm = document.getElementById('search_term').value; // 検索語の取得
            var url = `/api/students?${encodeURIComponent(searchCategory)}=${encodeURIComponent(searchTerm)}`; // 検索用URLの作成
            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                this.invalid = false; // 無効フラグを解除
                const oldResults = sessionStorage.getItem('searchResults');
                if (oldResults){
                    sessionStorage.removeItem('searchResults'); // 古い検索結果を削除
                }
                sessionStorage.setItem('searchResults', JSON.stringify(data)); // 新しい検索結果をセッションストレージに保存
                window.location.href = '/result'; // 結果ページにリダイレクト
            })
            .catch(error => {
                this.invalid = true; // 無効フラグを立てる
                console.error('データの取得中にエラーが発生しました:', error);
            });
        },
        register() {
            window.location.href = '/form'; // ユーザー登録ページにリダイレクト
        },
        logout() {
            window.location.href = '/logout'; // ログアウト
    }
}
});
