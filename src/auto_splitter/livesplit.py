import socket

class LivesplitServer():
    def __init__(self, server, port, load_remover_only = False):
        self.server = server
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.load_remover_only = load_remover_only
        
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
        
    def get_current_index(self):
        self.s.send(b"getsplitindex\r\n")
        return int(self.s.recv(1024).decode().strip())

    def set_server(self, server):
        self.server = server

    def set_port(self, port):
        self.port = port

    def send_split(self):
        if not self.load_remover_only:
            self.s.send(b"split\r\n")

    def start_timer(self):
        if not self.load_remover_only:
            self.s.send(b"initgametime\r\n")
            self.s.send(b"starttimer\r\n")
        
    def reset_game_time(self): 
        self.s.send(b"setgametime 0\r\n")

    def start_game_timer(self):
        print("Unpausing timer at %s" % (self.get_current_time()))
        self.s.send(b"unpausegametime\r\n")

    def stop_game_timer(self):
        print("Pausing timer at %s" % (self.get_current_time()))
        self.s.send(b"pausegametime\r\n")