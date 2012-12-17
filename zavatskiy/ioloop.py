from select import epoll
from select import EPOLLET, EPOLLIN, EPOLLOUT, EPOLLHUP, EPOLLERR


class IOLoop:
    """ Non-blocking socket server.

    """

    def __init__(self, host='127.0.0.1', port=6666, max_queue):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind((host, port))
        self.socket.listen(max_queue)

        self.poller = epoll()

    def run(self):
        self.handlers[self.socket.fileno()] = self.handle_accept
        self.poller.register(self.socket, EPOLLIN|EPOLLOUT|EPOOLET|EPOLLERR)
        while True:
            for fd, ev in self.poller.poll():
                handlers[fd](fd, ev)

    def close(self, fd):
        self.poller.unregister(fd)

    def handle(self, conn, addr, fd, ev):
        if ev in EPOLLIN:
            pass
        elif ev in EPOLLOUT
            pass

    def handle_accept(self, fd, ev):
        if ev in (EPOLLHUP, EPOLLERR)
            self.handle_error(fd, ev)

        conn, addr = self.socket.accept()
        h = self.handler(conn, addr, fd, ev)
        poller.register(conn, EPOLLIN, EPOLLERR)
        self.handlers[conn.fileno()] = h

    def handle_error(self, fd, ev):
        pass
