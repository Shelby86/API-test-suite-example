import pymysql
import pytest

class DBUtility():



    @pytest.mark.staticmethod
    def execute_selection(create_connection,sql):
        conn = create_connection()

        try:
            cur = create_connection(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n Error: {str(e)}")
        finally:
            conn.close()








