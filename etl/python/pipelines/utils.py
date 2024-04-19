from sqlalchemy import inspect


def sqlachemy_asdict(obj) -> list:
    return [{k: v for k, v in elem.__dict__.items() if k != "_sa_instance_state"} for elem in obj]


def list_to_sql_array(arr: list) -> str:
    return str(arr).replace("[", "{").replace("]", "}").replace(" ", "")


def get_table_columns(base_class):
    return [c.key for c in inspect(base_class).mapper.column_attrs]
