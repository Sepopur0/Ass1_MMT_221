import User
import pickle
import threading


class Database:
    def __init__(self):
        # Key: username --- Val: <User>
        self.userDict = {}
        # Key: username -- Val: list contains all names of friends of username
        self.userFriend = {}
        # Key: username -- Val: list contains all names of friend-requests of username
        self.userFriendRequest = {}
        self.lock = threading.Lock()
        self.port_dict = {}
        self.load()

    def save(self):
        # save data to file
        with open("Data/userDict.pkl", "wb") as f1:
            pickle.dump(self.userDict, f1, pickle.HIGHEST_PROTOCOL)
        with open("Data/userFriend.pkl", "wb") as f2:
            pickle.dump(self.userFriend, f2, pickle.HIGHEST_PROTOCOL)
        with open("Data/userFriendRequest.pkl", "wb") as f3:
            pickle.dump(self.userFriendRequest, f3, pickle.HIGHEST_PROTOCOL)

    def setPort(self, username, host, port):
        self.port_dict[username] = (host, port)

    def initOffline(self):
        for name, user in self.userDict.items():
            if type(user.status)!=int and user.status==True:
                user.status = False
            

    def load(self):
        try:
            # retreive data from file
            with open('Data/userDict.pkl', 'rb') as f1:
                self.userDict = pickle.load(f1)
                # all user are offline when server first start and no client has connected succesfully
                self.initOffline()
            with open('Data/userFriend.pkl', 'rb') as f2:
                self.userFriend = pickle.load(f2)
            with open('Data/userFriendRequest.pkl', 'rb') as f3:
                self.userFriendRequest = pickle.load(f3)
        except:
            return

    def isRegistered(self, username):
        if username in self.userDict:
            return True
        else:
            return False

    def getStatus(self, username):
        if not self.isRegistered(username):
            return None
        return self.userDict[username].status

    def createUser(self, username, password):
        # Add new user
        if self.isRegistered(username):
            return False
        self.lock.acquire()
        self.userDict[username] = User.User(username, password)
        self.userFriend[username] = []
        self.userFriendRequest[username] = []
        self.save()
        self.lock.release()
        return True

    def createGroup(self,groupname,firstmem,secondmem):
        if self.isRegistered(groupname):
            return False
        self.lock.acquire()
        self.userDict[groupname] = User.Group(firstmem,groupname)
        self.userFriend[groupname] = [firstmem,secondmem]
        self.userFriend[firstmem].append(groupname)
        self.userFriend[secondmem].append(groupname)
        self.userFriendRequest[groupname] = []
        self.setPort(
            groupname,'group','group') #fake group port
        self.save()
        self.lock.release()
        return True
    
    def renamegroup(self,groupname,newname):
        if self.isRegistered(newname):
            return False
        self.lock.acquire()
        self.userDict[newname] = self.userDict[groupname]
        self.userDict[newname].groupname=newname
        del self.userDict[groupname]
        self.userFriend[newname]=self.userFriend[groupname] 
        for friend in self.userFriend[newname]:
            self.userFriend[friend].append(newname)
            self.userFriend[friend].remove(groupname)
        del self.userFriend[groupname]
        self.save()
        self.lock.release()
        return True
    
    def addFriend(self, username1, username2): #for both user and group
        # Args: username1:send request, username2: receive request
        # Add username1 into friendRequest of username2
        if (not self.isRegistered(username1)) or (not self.isRegistered(username2)):  # check registration
            return False
        listFriend = self.userFriend[username2]
        listRequest = self.userFriendRequest[username2]
        if username1 in listFriend or username1 in listRequest or (username1 == username2) or type(self.userDict[username2].status)==int:
            return False
        else:
            self.lock.acquire()
            listRequest.append(username1)
            self.save()
            self.lock.release()
            print(self.userFriendRequest[username2])
            return True
        
    def removeFriend(self,username1,username2,author=None): #for both user and group
        if (not self.isRegistered(username1)) or (not self.isRegistered(username2)):  # check registration
            return False
        listFriend1 = self.userFriend[username1]
        listFriend2=self.userFriend[username2]
        if author==None and ((not (username1 in listFriend2)) or (not (username2 in listFriend1)) or username1 == username2): #user remove user
            return False
        elif author!=None and (author!=self.userDict[username1].author or author==username2): #group host remove member or member leave group
            return False
        else:
            self.lock.acquire()
            listFriend2.remove(username1)
            listFriend1.remove(username2)
            self.save()
            self.lock.release()
            print(self.userFriendRequest[username2])
            return True
    
    
    def showFriend(self, username):
        # Args: username
        # return: a ordered dict {friendName: status}
        if not self.isRegistered(username):
            return None
        friendList = self.userFriend[username]
        friendDict = {}
        for friend in friendList:
            friendDict[friend] = self.getStatus(friend)
        #friendDict = {k: v for k, v in sorted(friendDict.items(), key=lambda item: item[1], reverse=True)}
        return friendDict

    def showFriendRequest(self, username):
        # Args: username
        # return: an unordered list of friend requests of user with name username
        
        if not self.isRegistered(username):
            return None
        friendRequestList=self.userFriendRequest[username]
        friendRequestDict={}
        for friend in friendRequestList:
            friendRequestDict[friend]=self.getStatus(friend)
        return friendRequestDict

    def handleFriendRequest(self, username2, username1, accept):
        # Args: username1, username2
        # Accept friend request of username1 for username2. Adding them in their friendlist
        if (not self.isRegistered(username1)) or (not self.isRegistered(username2)):
            return False
        listFriend1 = self.userFriend[username1]
        listFriend2 = self.userFriend[username2]
        listRequest2 = self.userFriendRequest[username2]
        if (username1 in listFriend2) or (username1 not in listRequest2) or (username1 == username2):
            return False
        else:
            if accept:
                self.lock.acquire()
                listFriend1.append(username2)
                listFriend2.append(username1)
                listRequest2.remove(username1)
                self.save()
                self.lock.release()
                return True
            else:
                self.lock.acquire()
                listRequest2.remove(username1)
                self.save()
                self.lock.release()
                return False

    def Login(self, username, password):
        if not self.isRegistered(username):
            return False
        if self.userDict[username].password != password:
            return False
        return True

    def online(self, username):
        if not self.isRegistered(username):
            return False
        else:
            self.userDict[username].status = True
            return True

    def offline(self, username):
        if not self.isRegistered(username):
            return False
        else:
            self.userDict[username].status = False
            try:
                del self.port_dict[username]
            except:
                pass
            return True
