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
		 <!-- {{ Object.keys(file_information) }} -->
		<form @submit.prevent="send_parse_file_command">
		  <div v-for="(choices, field_name) in field_choices">
			<label :for="field_name">{{ field_name }}</label>
			<select :id="field_name" v-model="$data[field_name]">
			  <option v-for="(choice, choice_label) in choices">
				{{ choice_label }}
			  </option>
			</select>
		  </div>
		<input
		  type="submit"
		  class="btn btn-primary"
		  :class="{disabled: file_information.percentage_processed === 100.0 }"
		  value="Parse">
		</form>
      </div>
      <div class="modal-footer">
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
        field_choices: {
            type: Object,
            required: true,
        },
    },
    mounted() {
        for (var field in this.field_choices) {
            this.field = null;
        }
    },
    methods: {
        clicked_close() {
            console.debug('Modal was closed');
            this.$emit('clicked-close');
        },
        send_parse_file_command() {
            // POST data, dynamically populated by Django form
            data = {};
            for (var field in this.field_choices) {
                console.warn(field, this[field]);
                data[field] = this[field];
            }
            console.warn(data);
            console.debug(
                `Sending command for parsing file ${this.file_information.id}`,
            );
            axios
                .post(
                    `/api/histogram_data_files/${this.file_information.id}/start_parsing/`,
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
        on_submit() {
            let form = {};
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
