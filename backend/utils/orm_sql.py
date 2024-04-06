from django.db.models import Func


class SplitPart(Func):
    function = "split_part"
    arity = 3
