app.component('file-actions', {
    // delimiters: ['{', '}'],
    template:
        /*html*/
        `
<!-- :class="{ hidden: !is_visible }" -->
<div id="modal-file-actions" class="modal modal-extra" :class="{ shown: is_visible }" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
        <h5 class="modal-title">File actions (File {{ file_id }})</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="clicked_close">
          <span aria-hidden="true" >&times;</span>
        </button>
	  </div>
	  <div class="modal-body">
		<errors :errors="errors" @dismissed-error="dismiss_error"></errors>
		<p>Modal body text goes here.</p>
		{{ Object.keys(file_information) }}
      </div>
      <div class="modal-footer">
		<button
		  type="button"
		  class="btn btn-primary"
		  :class="{disabled: file_information.percentage_processed === 100.0 }"
		  v-on:click="send_parse_file_command(file_information)"
		  >
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
            errors: [],
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
        send_parse_file_command(file_information) {
            data = {};
            console.debug(
                `Sending command for parsing file ${file_information.id}`,
            );
            axios
                .post(
                    `/api/histogram_data_files/${file_information.id}/start_parsing/`,
                    data,
                    get_axios_config(),
                )
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.error(error);
                    this.errors.push(`${error}: ${error.response.data}`);
                });
        },
        dismiss_error(error) {
            console.debug(error);
            for (var i = 0; i < this.errors.length; i++) {
                if (this.errors[i] === error) {
                    this.errors.splice(i, 1);
                }
            }
        },
    },
});
