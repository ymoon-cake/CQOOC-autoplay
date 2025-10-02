import socket

def check_network():
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except OSError:
        return False