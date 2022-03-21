app.component('file-actions', {
    // delimiters: ['{', '}'],
    template:
        /*html*/
`
<!-- :class="{ hidden: !is_visible }" -->
<div id="modal-file-actions" class="modal" :class="{ shown: is_visible }" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
        <h5 class="modal-title">File actions (File {{ file_id }})</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="clicked_close">
          <span aria-hidden="true" >&times;</span>
        </button>
	  </div>
	  <div class="modal-body">
		<p>Modal body text goes here.</p>
		{{ Object.keys(file_information) }}
      </div>
      <div class="modal-footer">
        <!-- <button type="button" class="btn btn-primary">Save changes</button> -->
		<button type="button" class="btn btn-primary" :class="{disabled: file_information.percentage_processed === 100.0 }">
		  Parse
		</button>
      </div>
    </div>
  </div>
</div>
`,
    data() {
        return {
            // is_visible: false,
        };
    },
    props: {
        // modal_id: {
        //     type: String,
        //     required: true,
        // },
        file_id: {
            type: Number,
            required: true,
        },
        is_visible: {
            type: Boolean,
            required: true,
        },
        file_information: {
            type: Object,
            required: true,
        },
    },
    methods: {
        clicked_close() {
            console.debug('Modal was closed');
            this.$emit('clicked-close');
        },
    },
});
