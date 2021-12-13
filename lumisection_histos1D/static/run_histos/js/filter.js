function disable_empty_filter_fields(form){
    // disables every input field in a form
    // such that it does not appear as a
    // GET parameter in the url

    form.find(":input").filter(function () {
        return !this.value || this.value === "0";
    }).attr("disabled", "disabled");
}

function ignore_unwanted_filters(form){
    let checked_element = $(".ignore-other-filter-checkbox:checked");
    if(checked_element.length > 0){
        checked_element = checked_element.attr('id').replace('id-ignore-', '');
        form.find(":input").filter(function () {
            return !(this.id.indexOf(checked_element) !== -1);
        }).val("");
    }
}

function uncheck_all_ignore_other_filter_checkboxes(){
    $(".ignore-other-filter-checkbox").each(function(){
        var checkbox = $(this);
        checkbox.prop("checked", false);
    });
}