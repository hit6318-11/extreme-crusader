new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
        students: [],  // 検索結果で得られた学生のリスト
        selectedStudents: [],  // チェックボックスで選択された学生のIDのリスト
        currentSortField: null, // 現在のソートフィールド
        isAscending: true, // 昇順フラグ
        noResult:false, // 検索結果がない場合のフラグ
        items:[]

    },
    methods: {
        fetchResults() {
            const results = sessionStorage.getItem('searchResults');
            if (results.length < 3) { // 検索結果がない場合
                this.noResult = true; // フラグを立てる
                console.log('検索結果が見つかりません。');
            } else {
                this.noResult = false; // フラグを解除する
                this.students = JSON.parse(results); // 学生リストを取得
                sessionStorage.removeItem('searchResults'); // セッションストレージから削除
            }
        },
        editStudent(studentId) {
            sessionStorage.setItem('searchResults', JSON.stringify(this.students))
            window.location.href = `/form?id=${studentId}`; // 学生の編集ページにリダイレクト
        },
        goBack() {
            window.location.href = '/search'; // 検索ページに戻る
        },
        deleteSelected() {
            if (this.selectedStudents.length > 0) {
                if (confirm('選択した学生のデータを削除しますか？')) {
                    axios.post('/api/students/delete', { studentIds: this.selectedStudents })
                        .then(() => {
                            this.updateStudentList();
                            alert('選択したデータが削除されました。');
                        })
                        .catch(error => {
                            console.error('削除に失敗しました:', error);
                            alert('データの削除に失敗しました。');
                        });
                }
            } else {
                alert('削除する学生を選択してください。');
            }
        },
        updateStudentList() {
            // 選択された学生をリストから削除
            this.students = this.students.filter(student => !this.selectedStudents.includes(student.id));
            this.selectedStudents = []; // 選択状態をリセット
        },
        logout() {
            window.location.href = '/logout'; // ログアウト
        },
        toggleSort(field, ascending = false) {
            if (this.currentSortField === field) {
                this.isAscending = !this.isAscending; // 同じフィールドをクリックした場合、ソート方向を切り替える
            } else {
                this.currentSortField = field; // 異なるフィールドをクリックした場合、現在のソートフィールドを変更する
                this.isAscending = true; // ソート方向を昇順にリセットする
            }
            this.sortStudents(); // 学生リストをソートする
        },
        sortStudents() {
            this.students.sort((a, b) => {
                let valueA = this.normalizeValue(a[this.currentSortField]);
                let valueB = this.normalizeValue(b[this.currentSortField]);
                return (valueA < valueB) ? (this.isAscending ? -1 : 1) : (valueA > valueB) ? (this.isAscending ? 1 : -1) : 0;
            });
        },
        normalizeValue(value) {
            return typeof value === 'string' ? value.toLowerCase() : value; // 値を正規化して返す
        },
        toggleAllCheckboxes(event) {
            if (event.target.checked) {
                this.selectedStudents = this.students.map(student => student.id); // 全てのチェックボックスを選択する
            } else {
                this.selectedStudents = []; // 選択を解除する
            }
        }
    },
    mounted() {
        this.fetchResults(); // マウント時に検索結果を取得する
    }
});
