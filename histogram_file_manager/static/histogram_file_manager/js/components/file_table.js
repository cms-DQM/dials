app.component('file-table', {
    template:
        /*html*/
        `
<div>
  <h5>{{ results_count }} results </h5>
  <div class="table-responsive">
	<table class="table table-sm table-hover table-striped">
	  <thead class="thead-dark">
		<tr>
		  <th scope="col"
			  v-for="header in headers"
			  :key="header">
			{{ header }}
		  </th>
		  <th>Actions</th>
		</tr>
	  </thead>
	  <tbody>
		<tr v-for="file_information of files_information">
		  <td v-for="(value, i) of file_information" v-html="get_formatted_value(i, value)">
		  </td>
		  <td>
			<button type="button" class="btn btn-primary"
					v-on:click="file_actions_clicked(file_information)"
					>
			  Actions
			</button>
		  </td>
		</tr>
	  </tbody>
	</table>   
  </div>
</div>
		`,
    data() {
        return {
            column_customization_map: {
                filesize: function (value) {
                    return Number(value).toFixed(2) + ' MB';
                },
                filepath: function (value) {
                    var c = document.createElement('code');
                    var t = document.createTextNode(value);
                    c.appendChild(t);
                    return c.outerHTML;
                },
                percentage_processed: function (value) {
                    return Number(value).toFixed(2) + '%';
                },
                data_dimensionality: function (value) {
                    if (value === '2') {
                        return '2D';
                    } else if (value === '1') {
                        return '1D';
                    }
                    return '-';
                },
            },
        };
    },
    methods: {
        // Callback for Parsing button, takes the id of the file as parameter
        file_actions_clicked(file_information) {
            this.$emit('file-actions-clicked', file_information);
        },
        get_formatted_value(column_name, value) {
            if (column_name in this.column_customization_map) {
                return this.column_customization_map[column_name](value);
            }
            return value;
        },
    },
    props: {
        files_information: {
            type: Array,
            required: true,
        },
        results_count: {
            type: Number,
            required: true,
        },
    },
    computed: {
        headers() {
            if (this.files_information.length > 0) {
                return Object.keys(this.files_information[0]);
            } else {
                return [];
            }
        },
    },
});
