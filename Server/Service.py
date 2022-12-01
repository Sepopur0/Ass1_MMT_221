import threading
import com


class Service:
    def __init__(self, socket, addr, database, lock):
        # a socket usable to send and receive data on the connection
        self.socket = socket
        # (ip, port)
        self.addr = addr
        self.database = database
        self.lock = threading.Lock()
        self.username = None
        self.password = None

    #user
    def Register(self, data):
        username = data['username']
        password = data['password']
        success = True

        print(f"Register for: {username} with password {password}")
        # print(password)

        # user don't type in username or password
        if username is None or password is None:
            success = False
        else:
            if self.database.createUser(username, password):
                self.username = username
                self.password = password
                self.database.online(username)
                print("Welcome", username)
            else:
                success = False

        com.Send(self.socket, 'Register', {'success': success})

    # authenticate and save username, password to service
    #user
    def Login(self, data):
        username = data['username']
        password = data['password']
        success = True
        # print('Login: ', username, password)

        print(f"Login for: {username} with password {password}")

        if username is None or password is None:
            success = False
        else:
            if self.database.Login(username, password):
                self.username = username
                self.password = password
                self.database.online(username)
                print("Welcome", username)
            else:
                success = False

        com.Send(self.socket, 'Register', {'success': success})

    #user
    def showFriend(self):
        friendDict = self.database.showFriend(self.username)
        if friendDict == None:
            com.Send(self.socket, 'showFriend', {'success': False})
        else:
            # send friend list
            com.Send(self.socket, 'showFriend', {
                     'success': True, 'friendDict': friendDict})
    #group
    def creategroup(self,data):
        groupname=data['groupname']
        author=data['author']
        secondmem=data['secondmem']
        if self.database.createGroup(groupname,author,secondmem):
            com.Send(self.socket, 'addFriend', {'success': True})
        else:
            com.Send(self.socket, 'addFriend', {'success': False})    
    
    def showGroupmember(self,data):
        groupname=data['groupname']
        friendDict = self.database.showFriend(groupname)
        if friendDict == None:
            com.Send(self.socket, 'showgroupmen', {'success': False})
        else:
            # send friend list
            com.Send(self.socket, 'showgroupmem', {
                     'success': True, 'friendDict': friendDict})
    #user
    def showFriendRequest(self):
        requestList = self.database.showFriendRequest(self.username)
        if requestList == None:
            com.Send(self.socket, 'showFriendRequest', {'success': False})

        else:
            # send request list
            com.Send(self.socket, 'showFriendRequest', {
                     'success': True, 'requestList': requestList})
    #user
    def addFriend(self, data):
        username = data['username']        
        if self.database.addFriend(self.username, username):
            com.Send(self.socket, 'addFriend', {'success': True})
        else:
            com.Send(self.socket, 'addFriend', {'success': False})    
    
    def removeFriend(self,data):
        unfriended = data['unfriended']       
        username=data['username']
        if self.database.removeFriend(username, unfriended):
            com.Send(self.socket, 'removeFriend', {'success': True})
        else:
            com.Send(self.socket, 'removeFriend', {'success': False})  
    #group
    def fixmember(self, data,event):
        username = data['username']
        groupname=data['groupname']
        author=data['author']
        if event=='addmember':
            if self.database.addFriend(groupname, username):
                com.Send(self.socket, 'addmember', {'success': True})
            else:
                com.Send(self.socket, 'addmember', {'success': False})
        elif event=='removemember':
            if not self.database.removeFriend(groupname, username,author):
                com.Send(self.socket, 'removemember', {'success': False})
            else:
                com.Send(self.socket, 'removemember', {'success': True})
    
    def renamegroup(self,data):
        groupname=data['groupname']
        newname=data['newname']
        if self.database.renamegroup(groupname, newname):
            com.Send(self.socket, 'renamegroup', {'success': True})
        else:
            com.Send(self.socket, 'renamegroup', {'success': False})
    #user
    def handleFriendRequest(self, data):
        username = data['username']
        accept = data['accept']

        if self.database.handleFriendRequest(self.username, username, accept):
            com.Send(self.socket, 'handleFriendRequest', {'success': True})
        else:
            com.Send(self.socket, 'handleFriendRequest', {'success': False})

    
    #below is all belong to user
    
    def setPort(self, data):
        # host, port of who?? may be client is connecting with service but they don't use addr
        host = data['host']
        port = data['port']
        print('Set Port: ', host, port)

        # save the "listening for peers" socket of this client to database
        self.listen_host = host
        self.listen_port = int(port)
        # print(self.listen_host, self.listen_port)

        self.database.setPort(
            self.username, self.listen_host, self.listen_port)

    # get (host, port) of friend by username
    def requestPort(self, data):
        username = data['username']
        group=data['group']
        print('requestPort: ', username)

        if not self.database.isRegistered(username):  # unregistered username
            com.Send(self.socket, 'requestPort', {'success': False})
            return

        listFriend = self.database.userFriend[self.username]
        if username not in listFriend and data['group'] and not group:   # not friend/ still accept ì not friend but same group
            com.Send(self.socket, 'requestPort', {'success': False})
            return

        if type(self.database.userDict[username].status)==int:
            com.Send(self.socket, 'requestPort', {
                     'success': True, 'host': 'group', 'port': 'group'})
        elif username not in self.database.port_dict:
            print(self.database.port_dict)
            com.Send(self.socket, 'requestPort', {'success': False})
        else:
            host, port = self.database.port_dict[username]
            com.Send(self.socket, 'requestPort', {
                     'success': True, 'host': host, 'port': port})

    def __call__(self):
        while True:
            req = com.Receive(self.socket)
            event = req['event']
            data = req['data']

            if event == 'close':
                self.lock.acquire()
                self.close_response()
                self.lock.release()
                break
            elif event == 'addFriend':
                self.lock.acquire()
                self.addFriend(data)
                self.lock.release()
            elif event=='unfriend':
                self.lock.acquire()
                self.removeFriend(data)
                self.lock.release()
            elif event == 'handleFriendRequest':
                self.lock.acquire()
                self.handleFriendRequest(data)
                self.lock.release()
            elif event == 'showFriendRequest':
                self.lock.acquire()
                self.showFriendRequest()
                self.lock.release()
            elif event == 'showFriend':
                self.lock.acquire()
                self.showFriend()
                self.lock.release()
            elif event == 'setPort':
                self.lock.acquire()
                self.setPort(data)
                self.lock.release()
            elif event == 'requestPort':
                self.lock.acquire()
                self.requestPort(data)
                self.lock.release()
            elif event=='Register group':
                self.lock.acquire()
                self.creategroup(data)
                self.lock.release()
            elif event== 'addmember' or event=='removemember':
                self.lock.acquire()
                self.fixmember(data,event)
                self.lock.release()
            elif event=='showgroupmem':
                self.lock.acquire()
                self.showGroupmember(data)
                self.lock.release()
            elif event=='renamegroup':
                self.lock.acquire()
                self.renamegroup(data)
                self.lock.release()
            elif event == 'shutdown':
                if self.username == 'admin':
                    return True

        # close the server socket for this service
        print('Close service of client: ', self.addr)

    def send_accept(self):
        # event = accept no data
        com.Send(self.socket, 'accept')

    def send_close(self):
        # event = close no data
        com.Send(self.socket, 'close')

# user is offline
    def close_response(self):
        self.database.offline(self.username)
        self.socket.close()

    def verify(self):
        # while True:
        # receive event "login" or "register" data from client
        req = com.Receive(self.socket)
        if req['event'] == 'Register':
            self.Register(req['data'])
            # break
        elif req['event'] == 'Login':
            self.Login(req['data'])
            # break
