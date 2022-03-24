const app = Vue.createApp({
    data() {
        return {
            files_information: [],
            file_information: {},
            file_actions_is_visible: false,
            _waiting_for_data: false,
        };
    },
    // This will run as soon as the app is mounted
    mounted() {
        this._periodic_tasks();
        setInterval(this._periodic_tasks, 5000);
    },
    methods: {
        _periodic_tasks() {
            if (!this._waiting_for_data) {
                this._update_data();
            }
        },
        // Private method to fetch updated files information
        // via the API
        _update_data() {
            this._waiting_for_data = true;

            axios
                .get('/api/histogram_data_files/', get_axios_config())
                .then((response) => {
                    // console.warn(response);
                    this.files_information = response.data;
                })
                .catch((error) => console.error(error))
                .finally(() => {
                    this._waiting_for_data = false;
                });
        },
        show_file_actions_modal(file_information) {
            this.file_information = file_information;
            this.file_actions_is_visible = true;
        },
        hide_file_actions_modal() {
            this.file_actions_is_visible = false;
        },
    },
});
