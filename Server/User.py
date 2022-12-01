import sys
import socket
import selectors
import traceback

class User:
    def __init__(self, username, password):
        self.userName = username
        self.password = password
        self.status = False
        self.friendRequest = []
        self.friendList = []  # store userName of friend

#idea: create a fake "user" that is a friend of all group members, but this friend will take client ip as its ip. Each member when send to a group, 
# will actually send to all members of the group. This group will unite all
# messages into one message_list_dict.
#when startChatto a group, it will return a list of ip of members

class Group:
    def __init__(self, username,groupname):
        self.groupname = groupname
        self.status=1 
        self.author=username
        self.memberList = []  # store userName of friend