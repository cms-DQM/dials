app.component('table-pagination', {
    template:
        /*html*/
        `
<nav aria-label="Page navigation example" v-show="is_enabled">
  <ul class="pagination">
    <li class="page-item"><a class="page-link" v-on:click="clicked_previous">Previous</a></li>
    <!-- <li class="page-item" v-for="page_number in [...Array(total_pages).keys()]"><a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_number+1)">{{ page_number + 1 }}</a></li> -->
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
        total_pages: {
            type: Number,
            required: true,
        },
    },
    methods: {
        clicked_previous() {
            if (this.page_previous === null) {
                // No previous page
                return;
            }
            this.$emit('clicked-previous');
        },
        clicked_next() {
            if (this.page_next === null) {
                // No next page
                return;
            }
            this.$emit('clicked-next');
        },
        clicked_specific_page(page_number) {
            console.info(`Clicked page ${page_number}`);
            alert('Not implemented');
            this.$emit('clicked-specific-page', page_number);
        },
    },
    computed: {
        is_enabled() {
            // return true;
            return this.page_next !== null || this.page_previous !== null;
        },
    },
});
