app.component('file-actions', {
    // delimiters: ['{', '}'],
    template:
        /*html*/
        `
<div id="modal-file-actions" :class="{ hidden: !is_visible }">
  <div class="modal-content">

    <span class="close" v-on:click="clicked_close">&times;</span>
	<h4>File actions (File {{ file_id }})</h4>
    <p>Actions go here</p>
	<div class="col">
	  <div class="row">
		<button :class="{disabled: file_information.percentage_processed === 100.0 }">
		  Parse
		</button>
	  </div>
	</div>
{{ Object.keys(file_information) }}
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
