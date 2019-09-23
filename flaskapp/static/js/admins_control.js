import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.esm.browser.js'


new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        processing_ajax: false,
        is_showing_admins_list: false,
        ajax_request_is_successfull: false,
        admins_list_style_class: 'alert alert-light',
        show_admins_button_text: 'show admins',
        admins_list: []
    },
    methods: {
        adminsShowButton: function () {
            if (this.is_showing_admins_list) {
                this.show_admins_button_text = 'show admins';
                this.is_showing_admins_list = false;
            } else {
                this.processing_ajax = true;
                fetch('http://localhost:5000/api/get_admins', {
                    method: 'GET'
                }).then(
                    response => response.json()
                ).then((data) => {
                    if (data.data != null) {
                        
                        this.admins_list = data.data.admins;
                        if (this.admins_list.length == 0) {
                            this.admins_list_style_class = 'alert alert-danger';
                            this.admins_list[0] = 'No ADMINS FOUND';
                        } else {
                            this.admins_list_style_class = 'alert alert-light';
                        }
                    }
                    this.show_admins_button_text = 'hide admins';
                    this.is_showing_admins_list = true;
                    this.processing_ajax = false;
        
                })
            }
        }
    }
})
