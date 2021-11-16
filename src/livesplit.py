import socket
import config

class LivesplitServer():
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.s.connect((config.livesplit_server, config.livesplit_port))
            return "Connected to Livesplit!"
        except:
            print("Could not connect to LiveSplit. Make sure LiveSplit server is started and ports are correct.")
    
    def get_current_time(self):
        self.s.send(b"getcurrenttime\r\n")
        return self.s.recv(1024).decode().strip()
    
    def send_split(self):
        self.s.send(b"split\r\n")

    def start_timer(self):
        self.s.send(b"starttimer\r\n")