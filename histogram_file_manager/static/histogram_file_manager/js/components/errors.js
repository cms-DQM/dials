app.component('errors', {
    template:
        /*html*/
        `
<div v-show="has_errors">
  <div 
	role="alert"
	class="alert alert-danger alert-dismissable fade show"
	v-for="error in errors">
	<button
	  type="button"
	  class="btn-close"
	  data-bs-dismiss="alert"
	  aria-label="Close"
	  v-on:click="dismiss_error(error)">
	</button>
	{{ error }}

  </div>
</div>
		`,
    props: {
        errors: {
            type: Array,
            required: true,
        },
    },
    computed: {
        has_errors() {
            return this.errors.length > 0;
        },
    },
    methods: {
        dismiss_error(error) {
            this.$emit('dismissed-error', error);
        },
    },
});
