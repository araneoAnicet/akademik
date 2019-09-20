import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.esm.browser.js'


new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        processing_ajax: false,
        show_login_window: true,
        ajax_processing_message: '',
        server_message: '',
        admin_token: '',
        admin_email: '',
    },

    mounted () {
        if (localStorage.admin_token) {
            this.ajax_processing_message = 'Verifying admin token...';
            if (this.checkTokenStatus()) {
                this.admin_token = localStorage.admin_token;
            } else {
                localStorage.admin_token = '';
            }
        }

        if (localStorage.admin_email) {
            this.admin_email = localStorage.admin_email;
        }
    },

    methods: {
        getFormData: function () {
            this.server_message = '';
            this.ajax_processing_message = 'Requesting admin token...';
            this.processing_ajax = true;
            this.admin_email = this.$refs.admin_email.value;
            localStorage.admin_email = this.admin_email;
            
            if (this.getToken()) {
                this.processing_ajax = false;
                this.show_login_window = false;
                localStorage.admin_token = this.admin_token;
            } else {
                this.processing_ajax = false;
            }
            
        },

        getToken: function () {
            fetch('http://localhost:5000/api/get_api_token', {
                method: 'POST',
                headers: {
                    'email': this.admin_email,
                    'password': this.$refs.admin_password.value
                }
            }).then(response => response.json()).then((data) => {
                this.server_message = data.message;
                if (data.data != null) {
                    this.admin_token = data.data.token;
                    return true;
                }
                return false;
            })
        },

        checkTokenStatus: function () {
            fetch('http://localhost:5000/api/check_token/', {
                method: 'POST',
                headers: {
                    'Authorization': localStorage.admin_token
                }
            }).then(response => response.json()).then((data) => {
                if (datalstatus == 200) {
                    return true;
                }
                return false;
            })
        }
    }
})