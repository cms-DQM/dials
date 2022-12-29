app.component('table-pagination', {
    // current_page_number starts from 1
    // page_iterator and page_number starts from 0
    template:
        /*html*/
        `
<nav aria-label="Page navigation example" v-show="is_enabled">
  <ul class="pb-3 pt-3 pagination justify-content-center">
    <li class="page-item" :class="{disabled: current_page_number == 1}">
      <a class="page-link" v-on:click="clicked_previous">Previous</a>
    </li>

    <template v-if="total_pages <= 10">
      <li class="page-item" v-for="page_number of page_iterator" :class="{active: page_number+1 == current_page_number}">
      <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_number+1)">
          {{ page_number + 1 }}
      </a>
      </li>
    </template>
    <template v-else>
      <li class="page-item" :class="{active: current_page_number == 1}">
        <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(1)"> 1 </a>
      </li>

      <template v-if="current_page_number <= 4">
        <li class="page-item" :class="{active: current_page_number == 2}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(2)"> 2 </a>
        </li>
        <li class="page-item" :class="{active: current_page_number == 3}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(3)"> 3 </a>
        </li>
        <li class="page-item" v-if="current_page_number >= 3" :class="{active: current_page_number == 4}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(4)"> 4 </a>
        </li>
        <li class="page-item" v-if="current_page_number == 4" :class="{active: current_page_number == 5}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(5)"> 5 </a>
        </li>
        <li class="page-item disabled">
          <a aria-disabled="true" class="page-link"> ... </a>
        </li>
      </template>
      <template v-else-if="current_page_number >= page_length-3">
        <li class="page-item disabled">
            <a aria-disabled="true" class="page-link"> ... </a>
        </li>
        <li class="page-item" v-if="current_page_number <= page_length-3" :class="{active: current_page_number == page_length-4}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_length-4)"> {{ page_length-4 }} </a>
        </li>
        <li class="page-item" v-if="current_page_number <= page_length-2" :class="{active: current_page_number == page_length-3}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_length-3)"> {{ page_length-3 }} </a>
        </li>
        <li class="page-item" :class="{active: current_page_number == page_length-2}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_length-2)"> {{ page_length-2 }} </a>
        </li>
        <li class="page-item" :class="{active: current_page_number == page_length-1}">
          <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_length-1)"> {{ page_length-1 }} </a>
        </li>
      </template>
      <template v-else>
        <li class="page-item disabled">
          <a aria-disabled="true" class="page-link"> ... </a>
        </li>
        <template v-for="page_number of page_iterator">
          <li class="page-item" v-if="(current_page_number-2 <= page_number) && (current_page_number >= page_number)" :class="{active: page_number+1 == current_page_number}">
            <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_number+1)">
              {{ page_number + 1 }}
            </a>
          </li>
        </template>
        <li class="page-item disabled">
          <a aria-disabled="true" class="page-link"> ... </a>
        </li>
      </template>
      
      <li class="page-item" :class="{active: current_page_number == page_length}">
        <a aria-disabled="true" class="page-link" v-on:click="clicked_specific_page(page_length)"> 
          {{ page_length }}
        </a>
      </li>
    </template>
	
    <li class="page-item" :class="{disabled: current_page_number == page_length}">
      <a class="page-link" v-on:click="clicked_next">Next</a>
    </li>
  </ul>
</nav>
		`,
    props: {
        // Not actually used here, just keeping them
        // for checking if pagination should be shown
        page_next_url: {
            required: true,
        },
        page_previous_url: {
            required: true,
        },
        total_pages: {
            type: Number,
            required: true,
        },
        current_page_number: {
            type: Number,
            required: true,
        },
    },
    methods: {
        clicked_previous() {
            if (this.page_previous_url === null) {
                // No previous page
                return;
            }
            this.$emit('clicked-previous');
        },
        clicked_next() {
            if (this.page_next_url === null) {
                // No next page
                return;
            }
            this.$emit('clicked-next');
        },
        clicked_specific_page(page_number) {
            console.info(`Clicked page ${page_number}`);
            this.$emit('clicked-specific-page', page_number);
        },
    },
    computed: {
        is_enabled() {
            // return true;
            return (
                this.page_next_url !== null || this.page_previous_url !== null
            );
        },
        page_iterator() {
            return Array.from(Array(Math.ceil(parseInt(this.total_pages))).keys());
        },
        page_length() {
            return Math.ceil(parseInt(this.total_pages));
        }
    },
});
