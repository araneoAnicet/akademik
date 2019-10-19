import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.esm.browser.js'


new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        getAPIInfo_error_message: 'Looks like there is not data to handle ;-(',
        show_getAPIInfo_error_message: false,
        processing_ajax: false,
        processing_link_request: false,
        link_data: {},
        show_login_window: true,
        ajax_processing_message: '',
        server_message: '',
        admin_token: '',
        admin_email: '',
        page : Object.freeze({
            days: "get_days",
            registrations: "get_unregistered_users",
            profileChanges: "get_profilechanges"
        })
    },

    mounted () {
        if (localStorage.admin_token) {
            this.ajax_processing_message = 'Verifying admin token...';
            this.checkTokenStatus();
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
            this.getToken()
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
                    this.processing_ajax = false;
                    this.show_login_window = false;
                    localStorage.admin_token = this.admin_token;
                }
                this.processing_ajax = false;
                this.getRegistrations();
            })
        },

        checkTokenStatus: function () {
            this.processing_ajax = true;
            fetch('http://localhost:5000/api/check_token', {
                method: 'GET',
                headers: {
                    'Authorization': localStorage.admin_token
                }
            }).then(response => response.json()).then((data) => {
                this.server_message = data.message;
                this.processing_ajax = false;
                if (data.status == 200) {
                    this.admin_token = localStorage.admin_token;
                    this.show_login_window = false;
                    this.getRegistrations();
                } else {
                    localStorage.admin_token = '';
                }
            })
        },

        getAPIInfo: function (link_end) {
            this.link_data = {};
            this.processing_link_request = true;
            fetch(`http://localhost:5000/api/${link_end}`, {
                method: 'GET',
                headers: {
                    'Authorization': this.admin_token
                }
            }).then(response => response.json()).then((data) => {
                if (data.status == 200) {
                    this.link_data = data.data;
                    if (this.link_data.iterable.length) {
                        this.show_getAPIInfo_error_message = false;
                    }
                    else {
                        this.show_getAPIInfo_error_message = true;
                    }
                }
            })
            this.processing_link_request = false;
        },

        getDays: function () {
            this.getAPIInfo(this.page.days);
        },

        getRegistrations: function () {
            this.getAPIInfo(this.page.registrations);
        },

        getProfilechanges: function () {
            this.getAPIInfo(this.page.profileChanges);
        }
    }
})