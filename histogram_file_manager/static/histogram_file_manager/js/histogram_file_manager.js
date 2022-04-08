const app = Vue.createApp({
    data() {
        return {
            files_information: [],
            file_information: {},
            file_actions_is_visible: false,
            waiting_for_data: false,
            page_next: null,
            page_previous: null,
            total_pages: 0,
        };
    },
    // This will run as soon as the app is mounted
    mounted() {
        // this._periodic_tasks();
        // setInterval(this._periodic_tasks, 5000);
        this._update_data();
    },
    methods: {
        // _periodic_tasks() {
        //     if (!this.waiting_for_data) {
        //         this._update_data();
        //     }
        // },
        // Private method to fetch updated files information
        // via the API
        _update_data(url = '/api/histogram_data_files/') {
            this.waiting_for_data = true;

            axios
                .get(url, get_axios_config())
                .then((response) => {
                    // console.warn(response);
                    this.files_information = response.data.results;
                    this.page_count = response.data.count;
                    this.page_next = response.data.next || null;
                    this.page_previous = response.data.previous || null;
                    this.total_pages = response.data.total_pages || 0;
                })
                .catch((error) => console.error(error))
                .finally(() => {
                    this.waiting_for_data = false;
                });
        },
        show_file_actions_modal(file_information) {
            this.file_information = file_information;
            this.file_actions_is_visible = true;
        },
        hide_file_actions_modal() {
            this.file_actions_is_visible = false;
        },
        fetch_previous_result_page() {
            this._update_data(this.page_previous);
        },
        fetch_next_result_page() {
            this._update_data(this.page_next);
        },
    },
});
