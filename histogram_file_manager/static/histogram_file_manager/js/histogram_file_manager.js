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
            page_current: '/api/histogram_data_files/',
            abort_controller: new AbortController(), // To cancel a request
        };
    },
    // This will run as soon as the app is mounted
    mounted() {
        this._periodic_tasks();
        setInterval(this._periodic_tasks, 5000);
        this._update_data(); // Immediately update data on start
    },
    methods: {
        _periodic_tasks() {
            if (!this.waiting_for_data) {
                this._update_data();
            }
        },
        _cancel_request() {
            if (this.waiting_for_data) {
                this.abort_controller.abort();
            }
        },
        // Private method to fetch updated files information
        // via the API
        _update_data() {
            let url = this.request_url;
            this.waiting_for_data = true;

            axios
                .get(url, get_axios_config(this.abort_controller))
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
            this.page_current = this.page_previous;
            this._cancel_request();
            this._update_data();
        },
        fetch_next_result_page() {
            this.page_current = this.page_next;
            this._cancel_request();
            this._update_data();
        },
    },
    computed: {
        request_url() {
            return this.page_current + window.location.search;
        },
    },
});
