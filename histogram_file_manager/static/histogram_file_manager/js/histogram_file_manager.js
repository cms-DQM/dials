const app = Vue.createApp({
    data() {
        return {
            files_information: [],
            file_information: {},
            file_actions_is_visible: false,
        };
    },
    // This will run as soon as the app is mounted
    mounted() {
        this._update_data();
    },
    methods: {
        // Private method to fetch updated files information
        // via the API
        _update_data() {
            // const csrftoken = getCookie('csrftoken'); // Will be needed for authentication
            axios
                .get('/api/histogram_data_files/')
                .then((response) => {
                    // console.warn(response);
                    this.files_information = response.data;
                    setTimeout(this._update_data, 5000);
                })
                .catch((error) => console.error(error));
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
