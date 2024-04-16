from rest_framework.exceptions import ParseError


def validate_th_filterset(form):
    # It seems CharField values comes as empty string from django filters form
    # In order to compare simultaneously excluding filters we need to also remove empty string values
    cleaned_data = {key: value for key, value in form.cleaned_data.items() if value is not None and value != ""}

    run_number_used = "run_number" in cleaned_data
    min_run_number_used = "min_run_number" in cleaned_data
    max_run_number_used = "max_run_number" in cleaned_data

    if run_number_used and (min_run_number_used or max_run_number_used):
        raise ParseError("run number and range run number cannot be used together.")

    ls_id_used = "ls_id" in cleaned_data
    ls_number_used = "ls_number" in cleaned_data
    min_ls_number_used = "min_ls_number" in cleaned_data
    max_ls_number_used = "max_ls_number" in cleaned_data

    if ls_number_used and ls_id_used:
        raise ParseError("ls number and lumisection id cannot be used together.")

    if ls_id_used and (min_ls_number_used or max_ls_number_used):
        raise ParseError("lumisection id and range ls number cannot be used together.")

    if ls_number_used and (min_ls_number_used or max_ls_number_used):
        raise ParseError("ls number and range ls number cannot be used together.")

    title_used = "title" in cleaned_data
    title_contains_used = "title_contains" in cleaned_data

    if title_used and title_contains_used:
        raise ParseError("title and title contains cannot be used together.")
