import socket
import threading

import pkt

from work.helpers import make_message, parse_message

class Server:
    """Simple blocking server."""

    def __init__(self, host='127.0.0.1', port=6666, max_queue=1):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(None)
        self.socket.bind((host, port))
        self.socket.listen(max_queue)
        self.threads = []
        self.__shutdown = False

    def new_stream(self, conn, addr):
        """Make thread for each client."""
        t = threading.Thread(target=self.handle_request, args=(conn, addr))
        t.start()
        self.threads.append(t)

    def handle_request(self, conn, addr):
        """Handler request."""
        conn.settimeout(5)

        feeder = pkt.Feeder(conn)
        buf = b''

        while not self.__shutdown:
            try:
                cmd = None
                while not cmd:
                    cmd, buf = feeder.feed(conn)
            except socket.timeout:
                break

            #if command == 'connect':
                #conn.sendall(make_message('connected', 'HELLO'))
            #elif command == 'ping':
                #conn.sendall(make_message('pong'))
            #elif command == 'pingd':
                #conn.sendall(make_message('pongd', data))
            #elif command == 'quit':
                #conn.sendall(make_message('ackquit', data))
                #break
            #elif command == 'finish':
                #conn.sendall(make_message('ackfinish', data))
                #self.__shutdown = True
                #raise socket.timeout
                #break

        #if self.__shutdown:
            #conn.sendall(make_message('ackfinish'))

        conn.close()

    def serve(self):
        """Run server."""
        while not self.__shutdown:
            try:
                conn, addr = self.socket.accept()
                self.new_stream(conn, addr)
            except socket.timeout:
                self.__shutdown = True
            except KeyboardInterrupt:
                self.__shutdown = True

        self.shutdown()

    def shutdown(self):
        """Shutdown server."""
        for thread in self.threads:
            thread.join()

        self.socket.close()


if __name__ == '__main__':
    server = Server()
    server.serve()
