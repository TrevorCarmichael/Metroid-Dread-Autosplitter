import socket

class LivesplitServer():
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.s.connect((self.server, self.port))
    
    def valid_connection(self):
        try:
            self.s.connect((self.server, self.port))
            return True
        except: 
            return False

    def get_current_time(self):
        self.s.send(b"getcurrenttime\r\n")
        return self.s.recv(1024).decode().strip()
    
    def set_server(self, server):
        self.server = server

    def set_port(self, port):
        self.port = port

    def send_split(self):
        self.s.send(b"split\r\n")

    def start_timer(self):
        self.s.send(b"starttimer\r\n")