function disable_empty_filter_fields(form){
    // disables every input field in a form
    // such that it does not appear as a
    // GET parameter in the url

    form.find(":input").filter(function () {
        return !this.value || this.value === "0";
    }).attr("disabled", "disabled");
}