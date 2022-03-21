const app = Vue.createApp({
    delimiters: ['{', '}'],
    data() {
        return {
            files_information: [],
        };
    },
    mounted() {
        // const csrftoken = getCookie('csrftoken'); // Will be needed for authentication
        axios
            .get('/api/histogram_data_files/')
            .then((response) => {
                console.warn(response);
                this.files_information = response.data;
            })
            .catch((error) => console.error(error));
    },
});
