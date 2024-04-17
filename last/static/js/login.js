new Vue({
    el: '#app',
    data: {
        credentials: { // 認証情報を格納するオブジェクト
            username: '', // ユーザー名
            password: '' // パスワード
        },
        loginError: false, // ログインエラーフラグ
        errorMessage: 'ユーザー名またはパスワードが無効です' // エラーメッセージ
    },
    methods: {
        login: function() {
            // サーバーサイドのルートに送信するフォームデータを構築する
            const formData = new FormData();
            formData.append('username', this.credentials.username);
            formData.append('password', this.credentials.password);

            // 認証用のサーバーサイドルートにPOSTリクエストを送信する
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // ログイン成功時に検索ページにリダイレクトする
                    window.location.href = '/search';
                } else {
                    // 認証失敗時の処理
                    this.loginError = true;
                }
            })
            .catch(error => {
                console.error('ログイン中にエラーが発生しました:', error);
            });
        },
        register: function() {
            // ユーザー登録ページにリダイレクトする
            window.location.href = '/register';
        }
    }
});
