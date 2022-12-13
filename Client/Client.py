import socket
import Service_client
import threading
import Buffer
import UI
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
            # print("Server closed.")
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
    def requestPort(self, username,group=False):
        com.Send(self.socket, 'requestPort', {'username': username,'group':group})
        res = com.Receive(self.socket)

        if res['data']['success']:
            host = res['data']['host']
            port = res['data']['port']
            return (host, port)
        else:
            return None

    #############################
    # def Close_chats(self):
    #     try:
    #         for username in self.message_list_dict:
    #             self.target=username
    #             self.chatTo('[From system] User ' + self.username + ' is offline!')
    #     except:
    #         return
    def close(self):
        # self.Close_chats()
        com.Send(self.socket, 'close')
        self.socket.close()
        for username in self.buff_dict:
            if self.buff_dict[username]!=404:
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
                #message_list = UI.Message_list(self.chatui.Message_box_frame)

                service = Service_client.Service_client(
                    conn, buff, self.username,self.message_list_dict, ip=self.ip)
                self.buff_dict[service.peer] = service.buffer

                # if service.peer in self.message_list_dict:
                #     service.message_list = self.message_list_dict[service.peer]
                # else:
                #     self.message_list_dict[service.peer] = service.message_list

                self.chatui.update()
                service.start()

        # self.listen_socket.close()
        # print('Closed listen socket: ', self.listen_socket)

    def run(self):
        self.loginui = UI.LoginWindow(self, ('Lato', 16))
        self.loginui.run()
        if self.loginui.closewindow==False:
            self.chatui = UI.ChatWindow(self, ('Lato', 11))
            self.chatui.run()

    ######## function is called by UI #########
    def Register(self, username, password): #either group(type=1) or new user(type=0)
        com.Send(self.socket, 'Register', {
                 'username': username, 'password': password})
        # receive verify result from server
        res = com.Receive(self.socket)

        if res['data']['success'] == True:
            self.username = username
            return True
        else:
            return False

    def Creategroup(self,secondmem, groupname):
        com.Send(self.socket, 'Register group', {
                 'groupname': groupname,'author':self.username,'secondmem':secondmem})
        # receive verify result from server
        res = com.Receive(self.socket)
        if res['data']['success'] == True:
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

    # def rejectFriendRequest(self, username, accept):
    #     com.Send(self.socket, 'handleFriendRequest', {
    #         'username': username, 'accept': accept})
    #     res = com.Receive(self.socket)['data']
    #     if res['success'] == True:
    #         return True
    #     else:
    #         return False

    def addFriend(self, username):
        com.Send(self.socket, 'addFriend', {'username': username})
        res = com.Receive(self.socket)['data']

        if res['success'] == True:
            return True
        else:
            return False

    def fixmember(self, groupname,username,cmd,author): #cmd=='addmember'/'removemember'
        com.Send(self.socket, cmd, {'groupname': groupname,'username':username,'author':author})
        res = com.Receive(self.socket)['data']

        if res['success'] == True:
            return True
        else:
            return False
       
    def removefriend(self,username,unfriended):
        com.Send(self.socket, 'unfriend', {'username':username,'unfriended': unfriended})
        res = com.Receive(self.socket)['data']

        if res['success'] == True:
            
            return True
        else:
            return False
    def renamegroup(self,groupname,newname):
        com.Send(self.socket, 'renamegroup', {'groupname': groupname,'newname':newname})
        res = com.Receive(self.socket)['data']
        if res['success'] == True:
            return True
        else:
            return False
    def shutdown(self):
        com.Send(self.socket, 'shutdown')

    def startChatTo(self, username,status):
        addr = self.requestPort(username)

        if addr is None and status!='Group':
            return False

        # client have a buffer and a service for each of its peer ?
        if status!='Group':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            buff = Buffer.Buffer(self.lock)
            # if username in self.message_list_dict:
            #     service = Service_client.Service_client(
            #         s, buff, self.username,self.message_list_dict, peer=username, ip=self.ip)
            #     self.buff_dict[username] = service.buffer
            # else:
                # message_list = UI.Message_list(self.chatui.Message_box_frame)
            service = Service_client.Service_client(
                    s, buff, self.username,self.message_list_dict, peer=username, ip=self.ip)
            self.buff_dict[username] = service.buffer
                # self.message_list_dict[username] = message_list
            # print('startChatTo:', addr)
            service.connectTo(addr)
            service.start()
        else:
            # if username not in self.message_list_dict:
            #     message_list = UI.Message_list(self.chatui.Message_box_frame)
            #     self.message_list_dict[username] = message_list
            com.Send(self.socket,'showgroupmem',{'groupname':username})
            res=com.Receive(self.socket)['data']['friendDict']
            for member in res:
                if member !=self.username:
                    mem_addr=self.requestPort(member,True)
                    if mem_addr==None:
                        continue
                    if member not in self.buff_dict:
                        mem_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        mem_buff = Buffer.Buffer(self.lock)
                        mem_service = Service_client.Service_client(
                        mem_s, mem_buff, self.username,self.message_list_dict, peer=member, ip=self.ip)
                        self.buff_dict[member]=mem_service.buffer
                        mem_service.connectTo(mem_addr)
                        mem_service.start()
            self.buff_dict[username]=404
                    
                
        self.chatui.update()
        return True
    
    def chatTo(self, message):
        if self.target is None:
            return

        username = self.target

        if username in self.buff_dict and type(self.buff_dict[username])!=int and self.buff_dict[username].status == True:
            self.buff_dict[username].assign('SendSMS', {'message':message,'target':self.username,'self':username})
            # print('old chat: ', self.buff_dict[username].string())
        elif username in self.buff_dict and self.buff_dict[username]==404:
            com.Send(self.socket,'showgroupmem',{'groupname':username})
            res=com.Receive(self.socket)['data']['friendDict']
            for mem in res:
                if mem!=self.username and res[mem]==True and mem in self.buff_dict:
                    self.buff_dict[mem].assign('SendSMS',{'message':message,'target':username,'self':username})
        else:
            check = self.startChatTo(username,'Online')
            if check:
                if type(self.buff_dict[username].status)!=int:
                    self.buff_dict[username].assign('SendSMS', {'message':message,'target':self.username,'self':username})
                else:
                    com.Send(self.socket,'showgroupmem',{'groupname':username})
                    res=com.Receive(self.socket)['data']['friendDict']
                    for mem in res:
                        if mem!=self.username and res[mem]==True and mem in self.buff_dict:
                            self.buff_dict[mem].assign('SendSMS',{'message':message,'target':username,'self':username})
            else:
                self.chatui.update()
            # print('new chat: ', self.buff_dict[username].string())

    def sendFileTo(self, filename):
        username = self.target
        if username in self.buff_dict and type(self.buff_dict[username])!=int and self.buff_dict[username].status == True:
            self.buff_dict[username].assign('SendFile', {'filename':filename,'target':self.username,'self':username})
        elif username in self.buff_dict and self.buff_dict[username]==404:
            com.Send(self.socket,'showgroupmem',{'groupname':username})
            res=com.Receive(self.socket)['data']['friendDict']
            for mem in res:
                if mem!=self.username and res[mem]==True and mem in self.buff_dict:
                    self.buff_dict[mem].assign('SendFile',{'filename':filename,'target':username,'self':username})
        else:
            check = self.startChatTo(username)
            if check:
                self.buff_dict[username].assign('SendFile', {'filename':filename,'target':self.username,'self':username})
            # else:
                # print("Not friend")

#idea: create a fake "client" that is a friend of all group members, but this friend will take client ip as its ip. Each member when send to a group, 
# will actually send to all members of the group. This group will unite all
# messages into one message_list_dict.
#when startChatto a group, it will return a list of ip of members
    