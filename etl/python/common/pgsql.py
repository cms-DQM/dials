import csv
from io import StringIO

import psycopg2.extras as extras


def copy_expert(table, conn, keys, data_iter) -> int:
    """
    A function that copies data from a CSV-like data iterator to a database table using the copy_expert method.

    Args:
        table: The table object representing the destination table in the database.
        conn: The database connection object.
        keys: The list of column names to copy data into.
        data_iter: An iterator containing the data rows to be copied.

    Returns:
        int: The number of rows copied into the table.
    """
    with conn.connection.cursor() as cur:
        columns = ", ".join(f'"{k}"' for k in keys)
        table_name = f"{table.schema}.{table.name}" if table.schema else table.name

        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        sql = f"COPY {table_name} ({columns}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)
        return cur.rowcount


def copy_expert_onconflict_skip(
    table, conn, keys, data_iter, return_ids: bool = False, pk: str | None = None
) -> int | list:
    """
    Copy data from data_iter into the specified table, ignoring conflicts according to the specified keys.
    Optionally return the IDs of the affected rows.

    Args:
        table: The table to copy data into.
        conn: The connection to the database.
        keys: The keys to use for conflict resolution.
        data_iter: An iterable providing the data to be copied.
        return_ids: Whether to return the IDs of affected rows (default is False).
        pk: The primary key of the table (only required if return_ids is True).

    Returns:
        If return_ids is True and pk is not None, a list of IDs of the affected rows;
        otherwise, the number of affected rows.
    """
    if return_ids is True and pk is None:
        raise ValueError("Can't return ids if pk is None")

    with conn.connection.cursor() as cur:
        columns = ", ".join(f'"{k}"' for k in keys)
        table_name = f"{table.schema}.{table.name}" if table.schema else table.name

        # If ignored conflicting rows is important: create staging table
        tmp_table_name = table_name + "_tmp"
        cur.execute(f"CREATE TEMP TABLE {tmp_table_name} (LIKE {table_name})")

        # Prepare data to be copied
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        # Copy into table
        sql = f"COPY {tmp_table_name} ({columns}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)

        # If ignored conflicting rows is important: insert into main table from temp and delete
        if return_ids:
            cur.execute(
                f"INSERT INTO {table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING RETURNING {pk}"  # noqa: S608
            )
            result = [tup[0] for tup in cur.fetchall()]
        else:
            cur.execute(f"INSERT INTO {table_name} SELECT * FROM {tmp_table_name} ON CONFLICT DO NOTHING")  # noqa: S608
            result = cur.rowcount

        cur.execute(f"DROP TABLE {tmp_table_name}")

        return result


def copy_expert_onconflict_update(table, conn, keys, data_iter, conflict_key: str, expr: str) -> int:
    """
    Copy data from data_iter into the specified table, handling conflicts according to the specified keys.

    Args:
        table: The table to copy data into.
        conn: The connection to the database.
        keys: The keys to use for conflict resolution.
        data_iter: An iterable providing the data to be copied.
        expr: Update expression tha will run on conflict.

    Returns:
        int: The number of rows copied into the table.
    """
    with conn.connection.cursor() as cur:
        columns = ", ".join(f'"{k}"' for k in keys)
        table_name = f"{table.schema}.{table.name}" if table.schema else table.name

        # If ignored conflicting rows is important: create staging table
        tmp_table_name = table_name + "_tmp"
        cur.execute(f"CREATE TEMP TABLE {tmp_table_name} (LIKE {table_name})")

        # Prepare data to be copied
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        # Copy into table
        sql = f"COPY {tmp_table_name} ({columns}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)

        # Insert in main table updating on conflict with expr
        cur.execute(
            f"INSERT INTO {table_name} SELECT * FROM {tmp_table_name} ON CONFLICT ({conflict_key}) DO UPDATE SET {expr}"  # noqa: S608
        )
        result = cur.rowcount
        cur.execute(f"DROP TABLE {tmp_table_name}")

        return result


def insert_onconflict_update(table, conn, keys, data_iter, conflict_key: str, expr: str) -> int:
    """
    Insert data from data_iter into the specified table, handling conflicts according to the specified keys.

    Args:
        table: The table to insert data into.
        conn: The connection to the database.
        keys: The keys to use for conflict resolution.
        data_iter: An iterable providing the data to be inserted.
        expr: Update expression tha will run on conflict.

    Returns:
        int: The number of rows inserted into the table.
    """
    with conn.connection.cursor() as cur:
        columns = ", ".join(f'"{k}"' for k in keys)
        table_name = f"{table.schema}.{table.name}" if table.schema else table.name

        # Insert data into the table
        sql = "INSERT INTO %s (%s) VALUES %%s ON CONFLICT (%s) DO UPDATE SET %s" % (  # noqa: S608,UP031
            table_name,
            columns,
            conflict_key,
            expr,
        )
        extras.execute_values(cur, sql, data_iter)
        conn.connection.commit()

        return cur.rowcount
