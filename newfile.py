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
        self.event = threading.Event()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()  # 服务启动
        threading.Thread(target=self.accept, name='accept').start()  # 给其他线程，保证主线程不阻塞

    def accept(self):
        while True:  # 一个线程
            s, raddr = self.sock.accept()  # 阻塞
            f = s.makefile(mode='rw')
            logging.info(raddr)
            logging.info(s)
            logging.info(f)
            self.clients[raddr] = f
            threading.Thread(target=self.recv, name='recv', args=(f, raddr)).start()

    def recv(self, f, addr):
        while not self.event.is_set():
            try:
                # data = f.recv(1024)  # 阻塞, bytes\
                data = f.readline()  # string, 有换行符
                if data == '':
                    # python下的socket不能检查连接状态，当断开连接时，recv内容为空
                    raise Exception()
                logging.info(data)
            except Exception as e:
                logging.error(e)
                data = 'quit'
            if data == 'quit':
                # 推出群聊
                f.close()
                self.clients.pop(addr)
                logging.info(addr)
                logging.info("已退出")
                break
            msg = "{} {} {}".format(
                addr,
                datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                data
            )
            for s in self.clients.keys():
                if s == addr:
                    continue
                f.write()
                f.flush()

    def stop(self):
        for s in self.clients.values():
            s.close()
        self.sock.close()
        self.event.set()

cs = ChatServer()
cs.start()

while True:
    cmd = input(">>>")
    if cmd.strip() == 'quit':
        cs.stop()
        threading.Event.wait(3)
        break
    logging.info(threading.enumerate())
