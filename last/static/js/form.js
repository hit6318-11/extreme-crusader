new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名', // ユーザー名を格納するデータプロパティ
        student: { // 学生の情報を格納するオブジェクト
            id: null, // 学生ID
            lastName: '', // 姓
            firstName: '', // 名
            lastNameKana: '', // 姓（かな）
            firstNameKana: '', // 名（かな）
            birthday: '', // 誕生日
            gender: null, // 性別
            email: '', // メールアドレス
            phone: '', // 電話番号
            mobilePhone: '', // 携帯電話番号
            postalCode: '', // 郵便番号
            address: '', // 住所
            classId: null, // クラスID
            status: null // 状態
        },
        classOptions: [], // クラスの選択肢を格納する配列
        postReq: false // POSTリクエストかどうかを示すフラグ
    },
    methods: {
        getStudent() {
            const queryParam = window.location.search; // クエリパラメータを取得
            if (queryParam) {
                console.log('this is student id', queryParam);
                const regex = /\?id=(\d+)/;
                const result = regex.exec(queryParam);
                const id = result ? result[1] : null;
                console.log(id);
                fetch(`/api/students?id=${id}`, { // 学生の情報を取得するAPIにリクエストを送信
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    let studentData = data[0];
                    const date = new Date(studentData.birthday);
        
                    const year = date.getFullYear();
                    const month = ("0" + (date.getMonth() + 1)).slice(-2);
                    const day = ("0" + date.getDate()).slice(-2);
        
                    const formattedDate = `${year}-${month}-${day}`;
                    studentData.birthday = formattedDate;
                    console.log("students data", studentData);
                    this.student = studentData;
                })
                .catch(error => {
                    console.error('データの取得中にエラーが発生しました:', error);
                });
            } else {
                this.postReq = true; // クエリパラメータがない場合は、POSTリクエストとして扱う
            }
        },
        getClasses(){
            fetch('/api/courses', { // クラスの一覧を取得するAPIにリクエストを送信
                 method: 'GET',
                 headers: {
                 'Content-Type': 'application/json',
                }
             })
            .then(response => response.json())
            .then(data => {
                this.classOptions = data; // 取得したクラスの一覧を保存
            })
            .catch(error => {
                console.error('データの取得中にエラーが発生しました:', error);
            });
        },
        confirmDelete() {
            if (confirm('本当に削除してよろしいですか？')) {
                // 削除処理
                fetch(`/api/students/${this.student.id}`, { // 学生を削除するAPIにリクエストを送信
                    method:'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log('サーバーからのレスポンス:', data);
                    // 必要に応じてレスポンスを処理
                })
                .catch(error => {
                    console.error('データの送信中にエラーが発生しました:', error);
                    // 必要に応じてエラーを処理
                });
                window.location.href = '/confirm'; // 確認画面にリダイレクト
            }
        },
        confirmAndSubmit() {
            if (confirm('変更しますか？')) {
                const birthdayDate = new Date(this.student.birthday);
                const formattedBirthday = birthdayDate.toISOString().slice(0, 10);
                const formData = {
                    // Vueデータからフォームデータを準備
                    last_name: this.student.lastName,
                    first_name: this.student.firstName,
                    last_name_katakana: this.student.lastNameKana,
                    first_name_katakana: this.student.firstNameKana,
                    birthday: formattedBirthday,
                    gender: this.student.gender,
                    email: this.student.email,
                    phone: this.student.phone,
                    mobile_phone: this.student.mobilePhone,
                    postal_code: this.student.postalCode,
                    address: this.student.address,
                    course_id: this.student.classId,
                    status: this.student.status
                };
                console.log("this is bday", formData.birthday);
                let url = '';
                let reqMethod = '';
                if (!this.postReq) {
                    url = `/api/students/${this.student.id}`;
                    reqMethod = 'PUT';
                } else {
                    url = `/api/students`;
                    reqMethod = 'POST';
                }
                // エンドポイントにPOSTリクエストを送信
                fetch(url, {
                    method: reqMethod,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData) // フォームデータをJSON文字列に変換
                })
                .then(response => response.json())
                .then(data => {
                    console.log('サーバーからのレスポンス:', data);
                    // 必要に応じてレスポンスを処理
                })
                .catch(error => {
                    console.error('データの送信中にエラーが発生しました:', error);
                    // 必要に応じてエラーを処理
                });
                window.location.href = '/confirm'; // 確認画面にリダイレクト
            }
        },
        logout() {
            window.location.href = '/logout'; // ログアウト
        }
    },
    mounted() {
        this.getClasses(); // クラス一覧の取得
        this.getStudent(); // 学生情報の取得
    }
});

