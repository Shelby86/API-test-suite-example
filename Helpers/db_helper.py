class DBHelper:

    def query_runner_as_dict(db, query):
        cursor = db
        cursor.execute(query)

        return {'results':
                    [dict(zip([column[0] for column in cursor.description], row))
                     for row in cursor.fetchall()]}

    def query_runner_as_list(db, query):
        cursor = db
        cursor.execute(query)

        cursor.execute(query)
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()

        return row
