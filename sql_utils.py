import sqlite3


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    else:
        return conn


def create_table(conn, tablename, column_type_dict):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        create_table_sql = 'CREATE TABLE {}('.format(tablename)
        for column, type_ in column_type_dict.items():
            create_table_sql += '{} {},\n'.format(column, type_)
        create_table_sql += ');'
        print(create_table_sql)
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insert(conn, tablename, columns, values):
    """
    Create a new project into the tablename table
    :param conn:
    :param project:
    :return: project id
    """
    cur = conn.cursor()
    sql = (
        'INSERT INTO {}({}) VALUES({})'
        .format(tablename, ', '.join(columns), '?' * len(columns))
    )
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid
