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
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" v-on:click="clicked_close">        </button>
	  </div>
	  <div class="modal-body">
    <success :success="success" @dismissed-success="dismiss_success"></success>
		<errors :errors="errors" @dismissed-error="dismiss_error"></errors>
		<div class="container-fluid">
		  <table class="table">
			<thead>
			</thead>
			<tbody>
			  <tr>
				<th scope="row">Filepath</th>
				<td><code>{{ file_information['filepath'] }}</code></td>
			  </tr>
			  <tr v-if="file_information['data_dimensionality'] !== 0">
				<th scope="row">Dimensionality</th>
				<td>{{ file_information['data_dimensionality'] }}</td>
			  </tr>
			  <tr v-if="file_information['granularity'] !== 'unk'">
				<th scope="row">Granularity</th>
				<td>{{ file_information['granularity'] }}</td>
			  </tr>			  
			</tbody>
		  </table>
		</div>
		<!-- {{ Object.keys(file_information) }} -->
		<form @submit.prevent="send_parse_file_command">
		  <div class="form-group" v-for="(choices, field_name) in field_choices">
			<label :for="field_name">{{ field_name }}</label>
			<select class="form-select" :id="field_name" v-model="$data[field_name]">
			  <option v-for="(choice_label, choice) in choices"  :value="choice">
				{{ choice_label }}
			  </option>
			</select>
		  </div>
		  <input
			type="submit"
			class="btn btn-primary mt-3"
			:class="{disabled: file_information.percentage_processed === 100.0 }"
			value="Parse">
		</form>
		<!-- Delete from Database -->
		<button @click="delete_file_command(file_id)"
				class="btn btn-danger mt-3">
		  <i class="bi bi-trash-fill"></i>Delete from DB
		</button>		
      </div>
      <div class="modal-footer">
      </div>
    </div>
  </div>
</div>
		`,
    data() {
        return {
            errors: [],
            success: [],
            message_id: 0,
        };
    },
    props: {
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
            this.errors = [];
            this.success = [];
            this.message_id = 0;
            this.$emit('clicked-close');
        },
        // Callback for form submission (file parsing)
        send_parse_file_command() {
            // Create a data variable for POST. Fields are dynamically populated by
            // Django form,
            // passed
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
                    this.success.push({
                      id: this.message_id,
                      message: `File id ${this.file_information.id} is being parsed.`
                    });
                    this.message_id += 1;
                })
                .catch((error) => {
                    console.error(error);
                    this.errors.push({
                      id: this.message_id,
                      message: `${error}: ${error.response.data}`
                    });
                    this.message_id += 1;
                });
        },
        // Callback for file deletion button
        delete_file_command(file_id) {
            console.debug(`Requested deletion of file with id=${file_id}`);
            axios
                .delete(
                    `/api/histogram_data_files/${this.file_information.id}/`,
                    get_axios_config(),
                )
                .then((response) => {
                    console.log(response);
                    this.success.push({
                      id: this.message_id,
                      message: `File id ${file_id} is successfully deleted.`
                    });
                    this.message_id += 1;
                })
                .catch((error) => {
                    console.error(error);
                    this.errors.push({
                      id: this.message_id,
                      message: `${error}: ${error.response.data}`
                    });
                    this.message_id += 1;
                });
        },
        // Callback for error dismissal from errors component
        dismiss_error(error) {
            console.debug(`this.errors is ${this.errors}`)
            console.debug(`Dismissing error alert with ID ${error.id}`);
            for (var i = 0; i < this.errors.length; i++) {
                if (this.errors[i].id === error.id) {
                  this.errors.splice(i, 1);
                  i -= 1;
                }
            }
            console.debug(`Now this.errors is ${this.errors}`)
        },
        dismiss_success(s) {
          console.debug(`Dismissing success alert with ID ${s.id}`);
          for (var i = 0; i < this.success.length; i++) {
              if (this.success[i].id === s.id) {
                  this.success.splice(i, 1);
                  i -= 1;
              }
          }
        },
    },
});
