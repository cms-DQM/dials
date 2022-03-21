app.component('file-table', {
    delimiters: ['{', '}'],
    template:
        /*html*/
        `
<div>
 <table>
   <tr>
     <th
	   v-for="header in headers"
	   :key="header">
	   { header }
	 </th>
   </tr>
  <tr v-for="file_information of files_information">
    <td v-for="value of file_information">
	  { value }
	</td>
  </tr>
</table>   
</div>
`,
    props: {
        // headers: {
        //     type: Array,
        //     required: true,
        // },
        // Array of objects
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
