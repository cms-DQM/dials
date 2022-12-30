app.component('success', {
    template:
        /*html*/
        `
<div v-show="has_success">
  <div 
	role="alert"
	class="alert alert-success alert-dismissable fade show"
	v-for="s in success">
    <div class="row">
      <div class="col-1">
        <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close">
        </button>
      </div>
      <div class="col-11">
        {{ s.message }}
      </div>
    </div>

  </div>
</div>
		`,
    props: {
        success: {
            type: Array,
            required: true,
        },
    },
    computed: {
        has_success() {
            return this.success.length > 0;
        },
    },
    methods: {
        dismiss_success(success) {
            this.$emit('dismissed-success', success);
        },
    },
});
