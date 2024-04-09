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
            axios.post('/api/authenticate', this.credentials)
                .then(response => {
                    // 認証成功時の処理
                    console.log('Authentication successful!', response.data);
                    
                    // Vue Routerを使用せずにダッシュボードページへリダイレクト
                    window.location.href = '/dashboard.html'; // ダッシュボードページのURLに変更してください
                })
                .catch(error => {
                    // 認証失敗時の処理
                    this.loginError = true;
                    console.error('Authentication failed', error);
                });
        }
    }
});
