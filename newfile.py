import socket
import threading
import logging

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


# TCP SERVER
class ChatServer:
    def __init__(self, ip='192.168.1.100', port=9999):
        self.addr = (ip, port)
        self.sock = socket.socket()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()  # 服务启动
        threading.Thread(target=self.accept, name='accept').start()  # 给其他线程，保证主线程不阻塞

    def accept(self):
        while True:
            s, raddr = self.sock.accept()  # 阻塞
            logging.info(raddr)
            logging.info(s)
            threading.Thread(target=self.recv, name='recv', args=(s, raddr)).start()

    def recv(self, sock, addr):
        while True:
            data = sock.recv(1024)  # 阻塞, bytes
            logging.info(data)
            sock.send('ack '.format(data.decode()).encode())

    def stop(self):
        self.sock.close()

cs = ChatServer()
cs.start()

while True:
    cmd = input(">>>")
    if cmd.strip() == 'quit':
        break
    logging.info(threading.enumerate())
