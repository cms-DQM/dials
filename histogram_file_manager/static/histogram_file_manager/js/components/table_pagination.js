app.component('table-pagination', {
    template:
        /*html*/
        `
<nav aria-label="Page navigation example" v-show="is_enabled">
  <ul class="pagination">
    <li class="page-item"><a class="page-link" v-on:click="clicked_previous">Previous</a></li>
    <!-- <li class="page-item" v-for="page_number in page_count"><a class="page-link" href="#">{{ page_number }}</a></li> -->
    <li class="page-item"><a class="page-link" v-on:click="clicked_next">Next</a></li>
  </ul>
</nav>
`,
    props: {
        // Not actually used here, just keeping them
        // for checking if pagination should be shown
        page_next: {
            required: true,
        },
        page_previous: {
            required: true,
        },
    },
    methods: {
        clicked_previous() {
            // console.info('Clicked Previous');
            this.$emit('clicked-previous');
        },
        clicked_next() {
            // console.info('Clicked Next');
            this.$emit('clicked-next');
        },
    },
    computed: {
        is_enabled() {
            return true;
            // return this.page_next !== null || this.page_previous !== null;
        },
    },
});
