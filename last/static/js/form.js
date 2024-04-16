new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
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
        classOptions: [] // This will be populated by Flask
    },
    methods: {
        confirmDelete() {
            if (confirm('本当に削除してよろしいですか？')) {
                // 削除処理
                window.location.href = '/confirm';
            }
        },
        confirmAndSubmit() {
            if (confirm('変更しますか？')) {
                // 送信処理
                window.location.href = '/confirm';
            }
        },
        logout() {
            // ログアウト処理
            window.location.href = '/confirm';
        },
    },
});
