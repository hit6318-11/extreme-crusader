new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
        students: [],
        currentSortField: null, // 現在のソートフィールド
        isAscending: true // 昇順かどうか
    },
    methods: {
        fetchResults() {
            const results = sessionStorage.getItem('searchResults');
            if (results) {
                this.students = JSON.parse(results);
                sessionStorage.removeItem('searchResults');
            } else {
                console.log('No search results found.');
            }
        },
        toggleSort(field) {
            if (this.currentSortField === field) {
                // 同じフィールドが再度クリックされた場合は、昇順/降順を切り替える
                this.isAscending = !this.isAscending;
            } else {
                // 新しいフィールドでソートする場合は、デフォルトで昇順に設定
                this.isAscending = true;
                this.currentSortField = field;
            }
            this.sortStudents();
        },
        sortStudents() {
            this.students.sort((a, b) => {
                let compareA = a[this.currentSortField];
                let compareB = b[this.currentSortField];
                
                // 文字列の場合は大文字、小文字を無視する
                if (typeof compareA === 'string') {
                    compareA = compareA.toLowerCase();
                    compareB = compareB.toLowerCase();
                }

                if (compareA < compareB) {
                    return this.isAscending ? -1 : 1;
                } else if (compareA > compareB) {
                    return this.isAscending ? 1 : -1;
                } else {
                    return 0;
                }
            });
        },
        editStudent(studentId) {
            window.location.href = `../templates/form.html?studentId=${studentId}`;
        },
        goBack() {
            window.location.href = '../templates/search.html';
        },
        logout() {
            window.location.href = '../templates/login.html';
        }
    },
    mounted() {
        this.fetchResults();
    }
});
