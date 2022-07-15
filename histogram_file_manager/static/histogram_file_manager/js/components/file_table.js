app.component('file-table', {
    template:
        /*html*/
        `
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
    <td v-for="value of file_information">
	  {{ value }}
	</td>
	<td>
	  <div class="col">
		<div class="row">
		  <button type="button" class="btn btn-primary"
			v-on:click="file_actions_clicked(file_information)"
			>
			Actions
		  </button>
		</div>
	  </div>
	</td>
  </tr>
</tbody>
 </table>   
</div>
`,
    methods: {
        // Callback for Parsing button, takes the id of the file as parameter
        file_actions_clicked(file_information) {
            this.$emit('file-actions-clicked', file_information);
        },
    },
    props: {
        files_information: {
            type: Array,
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
