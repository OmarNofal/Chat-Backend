

from socket_server.connection import connection


class connection_pool:
    """
    This class represents all currently active connections to the socket server
    The class stores entry in a dict using the mapping of `user_id` -> `connection`
    and also provides methods to add, get and delete connections 
    """
    instance = None
    def __init__(self) -> None:
        self.pool = dict()

    def add_connection(self, conn, user_id):
        if not user_id in self.pool:
            self.pool[user_id] = [conn]
        else:
            self.pool[user_id] += [conn]

    def get_connection(self, user_id):
        if not user_id in self.pool:
            return None
        return self.pool[user_id][0]

    def get_all_connections(self, user_id):
        if not user_id in self.pool:
            return None
        return self.pool[user_id]

    def remove_connection(self, conn, user_id):
        if user_id not in self.pool:
            return
        connections: list[connection] = self.pool[user_id]

        for i in range(0, len(connections)):
            if connections[i] == conn:
                connections.pop(i)
            if len(connections) == 0:
                del self.pool[user_id]

    def remove_all_connections(self, user_id):
        del self.pool[user_id]

    def get_instance():
        if connection_pool.instance == None:
            connection_pool.instance = connection_pool()
        return connection_pool.instance