from multiprocessing import connection
import unittest

from socket_server.connection_pool import connection_pool
from socket_server.connection import connection

class TestConnectionPool(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        self.pool = connection_pool.get_instance()
        super().__init__(methodName)

    def test_add_connection(self):
        conn1 = connection(None, None)
        conn2 = connection(None, None)

        user_id = '1201831'
        self.pool.add_connection(conn1, user_id)
        self.pool.add_connection(conn2, user_id)

        self.assertEqual(
            self.pool.pool[user_id],
            [conn1, conn2],
            'Connections not added to the pool'
        )

        del self.pool.pool[user_id]

    def test_remove_connections(self):
        conn1 = connection(None, None)
        user_id = '12121'

        self.pool.add_connection(conn1, user_id)
        self.pool.remove_all_connections(user_id)

        self.assertNotIn(user_id, self.pool.pool)

    def test_remove_connection(self):
        conn1 = connection(None, None)
        conn2 = connection(None, None)
        conn3 = connection(None, None)

        user_id = '1212'
        self.pool.add_connection(conn1, user_id)
        self.pool.add_connection(conn2, user_id)
        self.pool.add_connection(conn3, user_id)

        self.pool.remove_connection(conn3, user_id)
        self.assertNotIn(conn3, self.pool.get_all_connections(user_id))

        self.pool.remove_connection(conn2, user_id)
        self.assertNotIn(conn2, self.pool.get_all_connections(user_id))

if __name__ == '__main__':
    unittest.main()
