new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
        students: [],  // 検索結果で得られた学生のリスト
        selectedStudents: [],  // チェックボックスで選択された学生のIDのリスト
        currentSortField: null,
        isAscending: true,
        noResult:false
    },
    methods: {
        fetchResults() {
            const results = sessionStorage.getItem('searchResults');
            if (results.length < 3) {
                this.noResult = true;
                console.log('No search results found.');
            } else {
                console.log("this is result", results);
                console.log("this is length", results.length)
                this.noResult = false;
                console.log(JSON.parse(results))
                this.students = JSON.parse(results);
                sessionStorage.removeItem('searchResults');
            }
        },
        editStudent(studentId) {
            sessionStorage.setItem('searchResults', JSON.stringify(this.students))
            window.location.href = `/form?id=${studentId}`;
        },
        goBack() {
            window.location.href = '/search';
        },
        logout() {
            window.location.href = '/logout';
        },
        toggleSort(field, ascending = false) {
            if (this.currentSortField === field) {
                this.isAscending = !this.isAscending; // Toggle sort direction if clicking on the same field
            } else {
                this.currentSortField = field; // Change current sort field if clicking on a different field
                this.isAscending = true; // Reset sort direction to ascending
            }
            this.sortStudents();
        },
        sortStudents() {
            this.students.sort((a, b) => {
                let valueA = this.normalizeValue(a[this.currentSortField]);
                let valueB = this.normalizeValue(b[this.currentSortField]);
                return (valueA < valueB) ? (this.isAscending ? -1 : 1) : (valueA > valueB) ? (this.isAscending ? 1 : -1) : 0;
            });
        },
        normalizeValue(value) {
            return typeof value === 'string' ? value.toLowerCase() : value;
        },
        toggleAllCheckboxes(event) {
            if (event.target.checked) {
                this.selectedStudents = this.students.map(student => student.id);
            } else {
                this.selectedStudents = [];
            }
        }
    },
    mounted() {
        this.fetchResults();
    }
});
