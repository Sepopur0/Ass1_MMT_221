import json

HEADER_LENGTH = 10


def Send_File(conn, filename):
    with open(filename, "rb") as in_file:
        while True:
            data = in_file.read(2048)
            if not data:
                break
            conn.send(data)
    conn.close()


def Receive_File(conn, filename):
    with open(filename, "wb") as out_file:
        while True:
            # print('reading parts...')
            data = conn.recv(2048)
            if not data:
                break
            out_file.write(data)
    # print('readed')
    conn.close()


def Send(s, event, data={}):
    ob = {
        'event': event,
        'data': data
    }

    message = json.dumps(ob)
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    # if (event != "Idle" and event != "close"):
    #     print("Send: " + message_header.decode() + " " + message.decode())
    s.send(message_header + message)


def Receive(s):
    # message_header is length of message
    message_header = s.recv(HEADER_LENGTH)

    if not len(message_header):
        return None

    # Convert header to int value
    message_length = int(message_header.decode('utf-8').strip())
    message = s.recv(message_length).decode('utf-8')

    data = json.loads(message)
    temp = data["event"]
    # if (temp!= "Idle" and temp!= "close"):
    #     print("Receive: " + message_header.decode('utf-8') + " " + message)



    return data
