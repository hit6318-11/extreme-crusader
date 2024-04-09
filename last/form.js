
new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名', // ログイン時に設定されるべき値
        student: {
            id: '',
            lastName: '',
            firstName: '',
            lastNameKana: '',
            firstNameKana: '',
            birthday: '',
            gender: '',
            email: '',
            phone: '',
            mobilePhone: '',
            postalCode: '',
            address: '',
            classId: '',
        },
        classOptions: [
            { text: '7744', value: '1' },
            { text: '8843', value: '2' },
            // その他のクラスオプション
        ],
    },
    methods: {
        confirmDelete() {
            if (confirm('本当に削除してよろしいですか？')) {
                // 削除処理
                window.location.href = 'confirm.html';
            }
        },
        confirmAndSubmit() {
            if (confirm('変更しますか？')) {
                // 送信処理
                window.location.href = 'result.html';
            }
        },
        logout() {
            // ログアウト処理
            window.location.href = 'login.html';
        },
    },
});
