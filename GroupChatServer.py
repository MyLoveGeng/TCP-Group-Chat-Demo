import socket
import threading
import logging
import datetime

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


# TCP SERVER
class ChatServer:
    def __init__(self, ip='192.168.1.100', port=9999):
        self.addr = (ip, port)
        self.sock = socket.socket()
        self.clients = {}

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()  # 服务启动
        threading.Thread(target=self.accept, name='accept').start()  # 给其他线程，保证主线程不阻塞

    def accept(self):
        while True:  # 一个线程
            s, raddr = self.sock.accept()  # 阻塞
            logging.info(raddr)
            logging.info(s)
            self.clients[raddr] = s
            threading.Thread(target=self.recv, name='recv', args=(s, raddr)).start()

    def recv(self, sock, addr):
        while True:
            try:
                data = sock.recv(1024)  # 阻塞, bytes
                if data == b'':
                    raise Exception()
                logging.info(data)
                logging.info('recv')
            except Exception as e:
                logging.error(e)
                data = b'quit'
            if data == b'quit':
                # 推出群聊
                sock.close()
                self.clients.pop(addr)
                logging.info(addr)
                logging.info("已退出")
                break
            msg = "{} {} {}".format(
                sock.getpeername(),
                datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                data.decode('gb2312')
            ).encode('gb2312')
            for s in self.clients.values():
                if s == sock:
                    continue
                s.send(msg)

    def stop(self):
        for s in self.clients.values():
            s.close()
        self.sock.close()

cs = ChatServer()
cs.start()

while True:
    cmd = input(">>>")
    if cmd.strip() == 'quit':
        cs.stop()
        threading.Event.wait(3)
        break
    logging.info(threading.enumerate())
