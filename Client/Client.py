import socket
import Service_client
import threading
import Buffer
import GUII
import com
HEADER_LENGTH = 10

HOST = "localhost"  # Server's IP
PORT = 13000

class Client:
    def __init__(self):
        self.socket = None
        self.listen_socket = None
        self.buff_dict = {}
        self.message_list_dict = {}
        self.lock = threading.Lock()
        self.target = None
        self.listen_flag = True
        # get IP Address of Local host
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)

    def Connect(self):
        # This method will connect client socket to server socket
        # Create a new socket each time button is pressed
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        res = com.Receive(self.socket)
        if res['event'] == 'close':
            print("Server closed.")
            self.close_response()
            return False

        return True

    # Create a new socket for listening to all peer
    def Listen(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind(("", 0))

        # Inform server that this client started a new socket for peers
        self.setPort()
        # Create new thread for handling this socket
        self.listen_thread = threading.Thread(target=self.listen_run, args=())
        self.listen_thread.start()

    def setPort(self):
        host = self.ip
        port = self.listen_socket.getsockname()[1]
        # print('Set Port: ', host, port)
        com.Send(self.socket, 'setPort', {'host': host, 'port': port})

    # get address of username from server
    def requestPort(self, username):
        com.Send(self.socket, 'requestPort', {'username': username})
        res = com.Receive(self.socket)

        if res['data']['success']:
            host = res['data']['host']
            port = res['data']['port']
            return (host, port)
        else:
            return None

    ###################
    def close(self):
        com.Send(self.socket, 'close')
        self.socket.close()
        for username in self.buff_dict:
            self.buff_dict[username].assign('close', '')

        host = self.ip
        self.listen_flag = False
        if self.listen_socket is not None:
            port = self.listen_socket.getsockname()[1]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.close()

    def close_response(self):
        self.socket.close()

    def listen_run(self):
        self.listen_socket.listen()

        while self.listen_flag:
            conn, addr = self.listen_socket.accept()

            if self.listen_flag:
                buff = Buffer.Buffer(self.lock)
                message_list = GUII.Message_list(self.chatui.Message_box_frame)

                service = Service_client.Service_client(
                    conn, buff, message_list, self.username, ip=self.ip)
                self.buff_dict[service.peer] = service.buffer

                if service.peer in self.message_list_dict:
                    service.message_list = self.message_list_dict[service.peer]
                else:
                    self.message_list_dict[service.peer] = service.message_list

                self.chatui.update()
                service.start()

        print('Closed listen socket: ', self.listen_socket)

    def run(self):
        self.loginui = GUII.LoginWindow(self, ('Lato', 16))
        self.loginui.run()
        if self.loginui.closewindow==False:
            self.chatui = GUII.ChatWindow(self, ('Lato', 11))
            self.chatui.run()

    ######## function is called by GUII #########
    def Register(self, username, password):
        com.Send(self.socket, 'Register', {
                 'username': username, 'password': password})
        # receive verify result from server
        res = com.Receive(self.socket)

        if res['data']['success'] == True:
            self.username = username
            return True
        else:
            return False

    def Login(self, username, password):
        com.Send(self.socket, 'Login', {
                 'username': username, 'password': password})
        # receive verify result from server
        res = com.Receive(self.socket)

        if res['data']['success'] == True:
            self.username = username
            return True
        else:
            return False

    def showFriend(self):
        com.Send(self.socket, 'showFriend')
        res = com.Receive(self.socket)['data']

        if res['success'] == True:
            return res['friendDict']
        else:
            return None

    def showFriendRequest(self):
        com.Send(self.socket, 'showFriendRequest')
        res = com.Receive(self.socket)['data']

        if res['success'] == True:
            return res['requestList']
        else:
            return None

    def acceptFriendRequest(self, username, accept):
        com.Send(self.socket, 'handleFriendRequest', {
                 'username': username, 'accept': accept})
        res = com.Receive(self.socket)['data']
        if res['success'] == True:
            return True
        else:
            return False

    def rejectFriendRequest(self, username, accept):
        com.Send(self.socket, 'handleFriendRequest', {
            'username': username, 'accept': accept})
        res = com.Receive(self.socket)['data']
        if res['success'] == True:
            return True
        else:
            return False

    def addFriend(self, username):
        com.Send(self.socket, 'addFriend', {'username': username})
        res = com.Receive(self.socket)['data']

        if res['success'] == True:
            return True
        else:
            return False

    def shutdown(self):
        com.Send(self.socket, 'shutdown')

    def startChatTo(self, username):
        addr = self.requestPort(username)

        if addr is None:
            return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        buff = Buffer.Buffer(self.lock)

        # client have a buffer and a service for each of its peer ?
        if username in self.message_list_dict:
            service = Service_client.Service_client(
                s, buff, self.message_list_dict[username], self.username, peer=username, ip=self.ip)
            self.buff_dict[username] = service.buffer
        else:
            message_list = GUII.Message_list(self.chatui.Message_box_frame)
            service = Service_client.Service_client(
                s, buff, message_list, self.username, peer=username, ip=self.ip)
            self.buff_dict[username] = service.buffer
            self.message_list_dict[username] = service.message_list

        print('startChatTo:', addr)
        service.connectTo(addr)
        service.start()
        self.chatui.update()
        return True

    def chatTo(self, message):
        if self.target is None:
            return

        username = self.target

        if username in self.buff_dict and self.buff_dict[username].status == True:
            self.buff_dict[username].assign('SendSMS', message)
            print('old chat: ', self.buff_dict[username].string())
        else:
            check = self.startChatTo(username)
            if check:
                self.buff_dict[username].assign('SendSMS', message)
            else:
                self.chatui.update()
            print('new chat: ', self.buff_dict[username].string())

    def sendFileTo(self, filename):
        username = self.target
        if username in self.buff_dict and self.buff_dict[username].status == True:
            self.buff_dict[username].assign('SendFile', filename)
        else:
            check = self.startChatTo(username)
            if check:
                self.buff_dict[username].assign('SendFile', filename)
            else:
                print("Not friend")
