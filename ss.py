import socket
import selectors
import threading
import json
from queue import Queue
from socket_server.connection_pool import connection_pool

from socket_server.message_resolver import message_resolver
from socket_server.connection import connection
from socket_server.socket_message import socket_message
from utils.constants import *
from store.message_store import message_store

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind(('127.0.0.1', 5555))
lsock.listen()

selector = selectors.DefaultSelector()

selector.register(lsock, selectors.EVENT_READ)

command_queue = Queue()

def check_sent_messages(conn: connection):
    #check sent messages
    for msg in conn.sent_messages:
        if msg[HEADER_REQUEST] == REQUEST_MESSAGE_RECEIVE:
            msg_id = json.loads(msg.content)[BODY_MESSAGE_ID]
            store = message_store.get_instance()
            try:
                store.delete_message(msg_id)
            except Exception as e:
                print("An error occured while deleteing a sent message ", str(e))
        
def send_message_main(conn: connection, msg: socket_message):
    conn.send_message(msg)


def service_messages(conn: connection):
    msgs = conn.get_messages()
    for m in msgs:
        response = message_resolver(m, conn, command_queue).process()
        if response != None:
            content = json.dumps(response).encode('utf-8')
            print('sending message')
            res = socket_message(header={'type': 'response', 'content-length': len(content)}, content=content)
            # command_queue.put((conn, res))
            conn.send_message(res)


def service_connection(conn: connection, mask):
    # do the reading and writing
    conn.process_events(mask)
    if conn.is_closed and conn.user_id != None:
        # remove it from pool
        connection_pool.get_instance().remove_connection(conn, conn.user_id)
    # if len(conn.sent_messages) > 0:
        # threading.Thread(target=check_sent_messages, args=[conn]).start()
    if conn.has_messages():
        threading.Thread(target = service_messages, args= [conn]).start()


def accept_connection(sock):
    new_connection, _ = sock.accept()
    mask = selectors.EVENT_READ
    selector.register(new_connection, mask, connection(selector, new_connection))

def handle_queue():
    while not command_queue.empty():
        task = command_queue.get()
        send_message_main(task[0], task[1])    

def main_loop():
    while True:
        handle_queue()
        s = selector.select(0.1) # find a better alternative for waiting
        for key, mask in s:
            if key.fileobj == lsock:
                accept_connection(lsock)
            else:
                try:
                    service_connection(key.data, mask)
                except Exception as e:
                    print("There was en error while servicing a connection: ", str(e))

if __name__ == "__main__":
    main_loop()