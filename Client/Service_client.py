import threading
import socket
import os
import com
from pathlib import Path
from datetime import datetime
HEADER_LENGTH = 10
# HOST = "192.168.2.15"
# DEVICE_HOST = '192.168.0.103'
downloads_path = str(Path.home() / "Downloads\\") + '\\'


# a service for each connection to a friend (peer to peer)
class Service_client(threading.Thread):
    def __init__(self, socket, buff, username,mess_list, peer=None, ip=''):
        super(Service_client, self).__init__()
        self.socket = socket
        self.username = username
        # username of friend
        if peer is not None:
            self.peer = peer
        else:
            self.peer = self.verify()
        #
        self.mess_list=mess_list
        self.buffer = buff
        self.ip = ip

        # print("socket of this client service thread: " + str(socket))

    def connectTo(self, addr):
        self.socket.connect(addr)
            

    def Send_SMS(self, message,target,myself):
        com.Send(self.socket, 'sendSMS', {'message': message,'target':target})
        self.mess_list[myself].write(
            '['+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+' Me:]\n' + message + '\n')
        
    # def Send_group_SMS(self,data):
    #     com.Send(self.socket, 'sendGroupSMS', {'message': data['message'],'groupname':data['groupname']})
    
    def Receive_SMS(self, message,target):
        self.mess_list[target].write(
            "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + self.peer + ':]\n' + message + '\n')
        return message

    # def Receive_group_SMS(self,message,groupname,message_list):
    #     x=0
    ###
    def Send_File(self, filename,target,myself):
        if os.path.exists(filename):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            s.listen()
            self.mess_list[myself].write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' +
                "You has sent a file, file location: " + filename + "\n")
            com.Send(self.socket, "sendFile", {
                     'filename': filename, 'host': self.ip, 'port': s.getsockname()[1]})
            conn, addr = s.accept()

            thread = threading.Thread(
                target=com.Send_File, args=(conn, filename))
            thread.start()
        else:
            # print('No such file')
            return False

    # def Send_group_file(self,data):
    #     x=0
    #####
    def Receive_File(self, data,message_list):
        filename = downloads_path + data['filename'].split('/')[-1]
        # print('File: ', filename)
        host = data['host']
        port = int(data['port'])

        message_list.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' +
            self.peer + " has sent you a file, file location: " + filename + "\n")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        thread = threading.Thread(
            target=com.Receive_File, args=(s, filename))
        thread.start()

    def Receive_group_file(self,data):
        x=0
    def run(self):
        while True:
            if len(self.buffer) == 0:
                try:
                    com.Send(self.socket, "Idle")
                except:
                    self.close_response()
                    # print('close not safe')
                    break

                res = com.Receive(self.socket)
                event = res['event']
                data = res['data']

                # send username to peer
                if event == 'Verify':
                    self.on_verify()

                # receive sms from peer
                elif event == 'sendSMS':
                    mess = self.Receive_SMS(data['message'],data['target'])
                    # print('receive: ', mess)
                # elif event=='sendGroupSMS':
                #     mess=self.Receive_group_SMS(data)
                elif event == 'sendFile':
                    # must insert data
                    self.Receive_File(data['message'],data['target'])
                # elif event=='sendGroupFile':
                #     self.Receive_group_file(data)
                elif event == 'close':
                    self.close_response()
                    # print('close service')
                    break

            else:
                event, content = self.buffer.string()
                if event == 'SendSMS':
                    self.Send_SMS(content['message'],content['target'],content['self'])
                # elif event== 'SendGroupSMS':
                #     self.Send_group_SMS(content['message'],content['groupname'], content['mess_list'])
                elif event == 'SendFile':
                    self.Send_File(content['filename'],content['target'],content['self'])
                # elif event=='SendGroupFile':
                #     self.Send_group_file(content['filename'],content['target'], content['target'])
                elif event == 'close':
                    self.close()
                    # print('close service')
                    break

                self.buffer.assign('', '')

        self.buffer.off()

    def accept(self):
        com.Send(self.socket, 'accept')

    def close(self):
        com.Send(self.socket, 'close')
        data = self.socket.recv(1024)
        while data:
            data = self.socket.recv(1024)
        self.socket.close()

    def close_response(self):
        # message_list.write(self.peer + ' is offline! \n')
        self.socket.close()

    def verify(self):
        data = {}

        com.Send(self.socket, 'Verify')
        event = 'Idle'
        while event == 'Idle':
            res = com.Receive(self.socket)
            event = res['event']
            data = res['data']

        # print('verify: ', data)
        return data['username']

    def on_verify(self):
        com.Send(self.socket, 'Verify', {'username': self.username})
