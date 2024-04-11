new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名', // 仮のユーザー名。実際にはログイン時に取得した値を使用する
        students: [], // 検索結果を格納する配列
        selectedSort: '', // 選択された並び替えオプション
    },
    methods: {
        // サーバーから検索結果を取得
        fetchResults() {
                // セッションストレージから検索結果を取得
                const results = sessionStorage.getItem('searchResults');
                if (results) {
                    // セッションストレージに検索結果が存在する場合、それを解析してstudents配列に設定
                    this.students = JSON.parse(results);
                    // 使用後はセッションストレージから検索結果を削除
                    sessionStorage.removeItem('searchResults'); 
                } else {
                    // 検索結果が存在しない場合の処理
                    console.log('No search results found.');
                }
            },
            
        // 選択されたオプションに基づいて結果を並び替え
        sortResults() {
            if (this.selectedSort) {
                this.students.sort((a, b) => {
                    if (a[this.selectedSort] < b[this.selectedSort]) return -1;
                    if (a[this.selectedSort] > b[this.selectedSort]) return 1;
                    return 0;
                });
            }
        },
        // 編集ボタンクリック時の処理
        editStudent(studentId) {
            window.location.href = `../templates/form.html?studentId=${studentId}`; // 編集ページへのリダイレクト
        },
        // 「検索へ戻る」ボタンの処理
        goBack() {
            window.location.href = '../templates/search.html';
        },
        // 「ログアウト」ボタンの処理
        logout() {
            // セッションをクリアし、ログインページにリダイレクト（仮実装）
            window.location.href = '../templates/login.html';
        }
    },
    mounted() {
        this.fetchResults(); // コンポーネントがマウントされたら検索結果を取得
    }
});

