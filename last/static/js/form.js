new Vue({
    el: '#app',
    data: {
        username: 'ユーザー名',
        student: {
            id: null,
            lastName: '',
            firstName: '',
            lastNameKana: '',
            firstNameKana: '',
            birthday: '',
            gender: null,
            email: '',
            phone: '',
            mobilePhone: '',
            postalCode: '',
            address: '',
            classId: null,
            status: null
        },
        classOptions: [],
        postReq: false
    },
    methods: {
        getStudent(){
            const queryParam = window.location.search;
            if(!queryParam){
                this.requestType = true;
                return
            }else{
            console.log('this is student id', queryParam);
            const regex = /\?id=(\d+)/;
            const result = regex.exec(queryParam);
            const id = result ? result[1] : null;
            console.log(id);
            fetch(`/api/students?id=${id}`,{
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
                const month = ("0" + (date.getMonth() + 1)).slice(-2); // Month is zero-based, so we add 1
                const day = ("0" + date.getDate()).slice(-2);

                const formattedDate = `${year}-${month}-${day}`;
                studentData.birthday = formattedDate; 
                console.log("students data", studentData)
                this.student = studentData;
            })
            .catch(error => {
                console.error('Error fetching data:', 
                error);
            });
            }
            
        },
        getClasses(){
            fetch('/api/courses', {
                 method: 'GET',
                 headers: {
                 'Content-Type': 'application/json',
                }
             })
            .then(response => response.json())
            .then(data => {
                this.classOptions = data;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
                },
        confirmDelete() {
            if (confirm('本当に削除してよろしいですか？')) {
                // 削除処理
                window.location.href = '/confirm';
            }
        },
        confirmAndSubmit() {
            if (confirm('変更しますか？')) {
                const formData = {
                    // Prepare form data from Vue data
                    last_name: this.student.lastName,
                    first_name: this.student.firstName,
                    last_name_katakana: this.student.lastNameKana,
                    first_name_katakana: this.student.firstNameKana,
                    birthday: this.student.birthday,
                    gender: this.student.gender,
                    email: this.student.email,
                    phone: this.student.phone,
                    mobile_phone: this.student.mobilePhone,
                    postal_code: this.student.postalCode,
                    address: this.student.address,
                    course_id: this.student.classId,
                    status: this.student.status
                };
                // Send POST request to the endpoint
                fetch('/api/students', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData) // Convert form data to JSON string
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Response from server:', data);
                    // Handle response if needed
                })
                .catch(error => {
                    console.error('Error submitting data:', error);
                    // Handle error if needed
                });
            }
        },
        logout() {
            // ログアウト処理
            window.location.href = '/confirm';
        },
    },
    mounted() {
        this.getClasses();
        this.getStudent(); 
    }
});
