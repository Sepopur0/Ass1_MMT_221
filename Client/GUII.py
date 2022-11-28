import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

# screen resolution
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550

color_login = ["#07080C", "#594545", "#C7BCA1", "#F1D3B3"]
# color notes:  background   button                     text
color_chat = []


image = Image.open("background.png")


class Message_list:
    def __init__(self, frame):
        self.messages_list = scrolledtext.ScrolledText(frame, wrap='word', fg=color_login[3], bg=color_login[0])
        self.messages_list.insert(END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')

    def write(self, text):
        print(text)
        self.messages_list.configure(state='normal')
        if text != '\n':
            self.messages_list.insert(tk.END, text)
        self.messages_list.configure(state='disabled')
        self.messages_list.see(END)

    def delete(self):
        self.messages_list.configure(state='normal')
        self.messages_list.delete('1.0', END)

    def show(self):
        self.messages_list.pack(fill=BOTH, expand=YES)

    def hide(self):
        print('hide message list')
        self.messages_list.pack_forget()


class Window(object):
    def __init__(self, title, font, client):
        self.title = title
        self.closewindow = False
        self.font = font
        self.client = client
        self.root = tk.Tk()
        self.background_image = ImageTk.PhotoImage(image=image)
        self.root.config(bg=color_login[0])
        self.root.title(title)
        self.create_window()


class LoginWindow(Window):
    def __init__(self, client, font):
        super(LoginWindow, self).__init__(
            'Chat application: Login', font, client)
        self.create_window()

    def create_window(self):
        # configure window
        # set coordinate
        coor_x = int((self.root.winfo_screenwidth() - SCREEN_WIDTH) / 2)
        coor_y = int((self.root.winfo_screenheight() - SCREEN_HEIGHT) / 2)
        self.root.geometry('%dx%d+%d+%d' %
                           (SCREEN_WIDTH, SCREEN_HEIGHT, coor_x, coor_y))
        self.root.minsize(400, 350)
        # add background image
        background_label = Label(self.root)
        background_label.config(image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # create frames
        upper_frame = Frame(self.root, bg=color_login[0])
        upper_frame.grid(row=0, column=0)
        middle_frame = Frame(self.root, bg=color_login[0])
        middle_frame.grid(row=1, column=0)
        bottom_frame = Frame(self.root, bg=color_login[0])
        bottom_frame.grid(row=2, column=0)
        # grid frames
        self.root.grid_rowconfigure(0, weight=3)
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(1, weight=9)
        middle_frame.grid_columnconfigure(0, weight=8)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        # for upper frame
        tk.Label(upper_frame, text="Welcome to Group 13 Chat application", font=(
            'Arial', 28), fg='#FFFFFF', bg=color_login[0]).grid(row=0, column=0)
        tk.Label(upper_frame, text="Login or register to start chats with friend!",
                 font=self.font, fg='#FFFFFF', bg=color_login[0]).grid(row=1, column=0)
        # username label and text entry box
        tk.Label(middle_frame, text="User Name", font=self.font, fg=color_login[3], bg=color_login[0]).grid(
            row=0, column=0, padx=20, pady=20, sticky='e')
        self.username_input = tk.Entry(
            middle_frame, font=self.font, bg=color_login[3], fg=color_login[1])
        self.username_input.grid(row=0, column=1, sticky='w', padx=20)
        self.username_input.focus_set()
        # password label and password entry box
        Label(middle_frame, text="Password", font=self.font, fg=color_login[3], bg=color_login[0]).grid(
            row=1, column=0, padx=20, pady=20, sticky='e')
        self.password_input = Entry(
            middle_frame, font=self.font, show='*', bg=color_login[3], fg=color_login[1])
        self.password_input.grid(row=1, column=1, sticky='e', padx=20)
        # button
        Button(bottom_frame, text="Login", command=self.Login, font=self.font,
               fg=color_login[1], bg=color_login[3]).grid(row=0, column=1, padx=40, pady=10)
        Button(bottom_frame, text="Register", command=lambda: [self.killbutton(bottom_frame), self.add_register(
        )], font=self.font, fg=color_login[1], bg=color_login[3]).grid(row=0, column=0, padx=40, pady=10)

    def killbutton(self, frame):
        for widget in frame.grid_slaves():
            widget.destroy()

    def add_register(self):
        bottom_frame2 = Frame(self.root)
        bottom_frame2.grid(row=2, column=0)
        Button(bottom_frame2, text="Confirm registration", command=self.Register,
               font=self.font, fg=color_login[3], bg=color_login[1]).grid(row=0, column=0)

    def Register(self):
        self.client.Connect()
        username = self.username_input.get()
        password = self.password_input.get()
        if not self.client.Register(username, password):
            self.client.close()
        else:
            self.client.Listen()
            self.root.quit()
            self.root.destroy()

    def Login(self):
        self.client.Connect()
        username = self.username_input.get()
        password = self.password_input.get()
        if not self.client.Login(username, password):
            # print('failed')
            messagebox.showerror(
                "Login status", "Login failed! Please try again or register a new account.")
            self.client.close()
        else:
            self.client.Listen()
            self.root.quit()
            self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        # self.client.close()
        self.closewindow = True
        self.root.quit()


class ChatWindow(Window):
    def __init__(self, client, font):
        super(ChatWindow, self).__init__(
            'Chat application: Chat Window', font, client)
        coor_x = int((self.root.winfo_screenwidth() - SCREEN_WIDTH) / 2)
        coor_y = int((self.root.winfo_screenheight() - SCREEN_HEIGHT) / 2)
        self.root.geometry('%dx%d+%d+%d' %
                           (SCREEN_WIDTH, SCREEN_HEIGHT, coor_x, coor_y))
        self.root.minsize(600, 400)
        self.update()

    def show_event(self, dummyarg):
        self.Chat_button.pack_forget()
        self.Show_button_label.pack(side=LEFT, fill=X, expand=YES)
        self.Friend_request_button_label.pack_forget()
        self.Friend_request_button.pack(side=LEFT, fill=X, expand=YES)
        self.update()
        self.friend_request_list.pack_forget()
        self.chats_list.pack(side=LEFT, fill=BOTH, expand=YES)

    def Friend_request_event(self, dummyarg):
        self.Show_button_label.pack_forget()
        self.Chat_button.pack(side=LEFT, fill=X, expand=YES)
        self.Friend_request_button.pack_forget()
        self.Friend_request_button_label.pack(side=LEFT, fill=X, expand=YES)
        self.update()
        self.chats_list.pack_forget()
        self.friend_request_list.pack(side=LEFT, fill=BOTH, expand=YES)

    def create_window(self):
        """Build chat window, set widgets positioning and event bindings"""
        # Size config
        coor_x = int((self.root.winfo_screenwidth() - SCREEN_WIDTH) / 2)
        coor_y = int((self.root.winfo_screenheight() - SCREEN_HEIGHT) / 2)
        self.root.geometry('%dx%d+%d+%d' %
                           (SCREEN_WIDTH, SCREEN_HEIGHT, coor_x, coor_y))
        self.root.minsize(600, 400)

        # create all of the main containers
        self.header = Frame(self.root, bg=color_login[0])
        self.body = Frame(self.root, bg=color_login[0])
        self.left_frame = Frame(self.body, bg=color_login[0])
        self.right_frame = Frame(self.body, bg=color_login[0])

        # layout all of the main containers
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=8)
        self.root.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        self.header.grid(row=0, column=0, sticky='nsew')
        self.body.grid(row=1, column=0, sticky='nsew')

        self.left_frame.grid(row=0, column=0, padx=5, sticky='nsew')
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        # header components
        self.Username_label = Label(self.header, text="Welcome, " +
                                                      self.client.username + ". Current IP address: " + self.client.ip,
                                    font=('Arial', 20), bg=color_login[0], fg="#FFFFFF")
        self.Username_label.grid(row=0, column=0, sticky='w')

        # left frame components
        self.Search_Frame = Frame(self.left_frame, bg=color_login[0])
        self.Search_Frame.grid_rowconfigure(0, weight=1)
        self.Search_Frame.grid_columnconfigure(0, weight=1)
        self.Search_entry = Entry(
            self.Search_Frame, font=self.font, fg='lightgrey')
        self.Search_entry.insert(0, 'Type people\'s name here')
        self.Search_entry.bind('<FocusIn>', self.temp_text)
        # self.Search_entry.bind('<Return>', self.add_event)
        self.Search_entry.grid(row=0, column=0, sticky='nsew')
        findbutton = Button(self.Search_Frame, text='Find user',
                            command=self.add_event, font=self.font, fg=color_login[1], bg=color_login[3])
        findbutton.grid(row=0, column=1)

        self.Lists_Frame = Frame(
            self.left_frame, bg=color_login[0], pady=3)
        self.Chat_button = Button(
            self.Lists_Frame, text='Chats', font=self.font, fg=color_login[1], bg=color_login[3])
        self.Chat_button.bind('<Button-1>', self.show_event)
        self.Show_button_label = Label(
            self.Lists_Frame, text='Chats', font=('Lato', 13, 'bold'), fg=color_login[3], bg=color_login[0],
            relief='sunken')

        self.Friend_request_button = Button(
            self.Lists_Frame, text='Friend requests', font=self.font, fg=color_login[1], bg=color_login[3])
        self.Friend_request_button.bind(
            '<Button-1>', self.Friend_request_event)
        self.Friend_request_button_label = Label(
            self.Lists_Frame, text='Friend requests', font=('Lato', 13, 'bold'), fg=color_login[3], bg=color_login[0],
            relief='sunken')

        self.Show_button_label.pack(side=LEFT, fill=X, expand=YES)
        self.Friend_request_button.pack(side=LEFT, fill=X, expand=YES)

        self.chats_list_frame = Frame(self.left_frame, bg=color_login[0])
        self.chats_list_frame.grid_rowconfigure(0, weight=1)
        self.chats_list_frame.grid_columnconfigure(0, weight=1)
        self.chats_list = Listbox(
            self.chats_list_frame, selectmode=SINGLE, exportselection=False, bg=color_login[0], fg=color_login[3])
        self.chats_list.bind('<<ListboxSelect>>', self.select_chats_event)
        self.chats_list.pack(side=LEFT, fill=BOTH, expand=YES)

        self.friend_request_list = Listbox(
            self.chats_list_frame, selectmode=SINGLE, exportselection=False, bg=color_login[0], fg=color_login[3])
        self.friend_request_list.bind('<<ListboxSelect>>', self.select_friend_request)

        self.Search_Frame.grid(row=0, column=0, sticky='nsew')
        self.Lists_Frame.grid(row=1, column=0, sticky='nsew')
        self.chats_list_frame.grid(row=2, column=0, sticky='nsew')

        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # right frame components
        self.header_mess_frame = Frame(self.right_frame, bg=color_login[0], pady=3)
        self.header_mess_frame.grid_rowconfigure(0, weight=1)
        self.header_mess_frame.grid_columnconfigure(0, weight=1)
        self.friend_user = Label(self.header_mess_frame,
                            text='Choose a friend to chat',font=self.font,bg=color_login[3],fg=color_login[1])
        self.friend_user.grid(row=0, column=0, sticky='nswe')
        self.Delete_mes_button = Button(self.header_mess_frame, text="Delete conversation", command=self.delete_mess,
                                        fg=color_login[1], bg=color_login[3])
        self.Delete_mes_button.grid(row=0, column=1, sticky='nsew')
        self.Message_box_frame = Frame(self.right_frame, bg='black', pady=3)
        self.message_list = Message_list(self.Message_box_frame)
        self.message_list.show()

        self.Mess_frame = Frame(
            self.right_frame, bg=color_login[0])
        self.Mess_frame.grid_rowconfigure(0, weight=3)
        self.Mess_frame.grid_rowconfigure(1, weight=4)
        self.Mess_frame.grid_columnconfigure(0, weight=8)
        self.Mess_frame.grid_columnconfigure(1, weight=1)
        self.Mess = Text(self.Mess_frame, fg=color_login[3], bg=color_login[0])
        self.Send_mess_button = Button(self.Mess_frame, text=">>", fg=color_login[1], bg=color_login[3])
        self.Mess.bind('<Return>', self.send_mess_event)
        self.Send_mess_button.bind('<Button-1>', self.send_mess_event)
        self.Mess.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.Send_mess_button.grid(row=0, column=1, sticky='nsew')
        self.Send_file_button = Button(self.Mess_frame, text='Send file', fg=color_login[1], bg=color_login[3])
        self.Send_file_button.bind('<Button-1>', self.send_file_event)
        self.Send_file_button.grid(row=1, column=1, sticky='nsew')

        self.header_mess_frame.grid(row=0, column=0, sticky='nsew')
        self.Message_box_frame.grid(row=1, column=0, sticky='nsew')
        self.Mess_frame.grid(row=2, column=0, sticky='nsew')

        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    ##mini functions

    def delete_mess(self):
        peer = self.client.target
        print(peer)
        print(peer in self.client.message_list_dict)
        if peer and peer in self.client.message_list_dict:
            self.client.message_list_dict[peer].delete()

    def temp_text(self, dummyarg):
        self.Search_entry.delete(0, END)
        self.Search_entry.configure(fg="#000000")

    def update(self):
        friendlist = self.client.showFriend()
        self.chats_list.delete(0, 'end')
        self.friend_request_list.delete(0, 'end')
        print('nice')
        for friend in friendlist:
            # if friendlist[friend] == 'Online':
            #    print(friend)
            status = "Offline"
            if friendlist[friend] == True:
                status = "Online"
            self.chats_list.insert(tk.END, friend + ': ' + status)

        friendlist = self.client.showFriendRequest()
        print('update friend request list')
        for friend in friendlist:
            self.friend_request_list.insert(tk.END, friend)

    ##main
    def run(self):
        """Handle chat window actions"""
        self.root.mainloop()

    def on_close(self):
        self.client.close()
        print('ok')
        self.root.destroy()

    def select_chats_event(self, dummyarg):
        """Set as target currently selected login on login list"""
        cursor = self.chats_list.get(self.chats_list.curselection())
        target = cursor.split(':')[0]
        status = cursor.split(':')[1][1:]

        if target == None:
            return

        self.friend_user.config(text=target)
        self.client.target = target
        self.message_list.hide()
        if target == None:
            return

        if status == 'Online':
            if target not in self.client.buff_dict:
                self.client.startChatTo(target)
            elif self.client.buff_dict[target].status == False:
                self.client.startChatTo(target)

            print(target)
            self.message_list = self.client.message_list_dict[target]
            self.message_list.show()

        else:
            if target not in self.client.message_list_dict:
                self.client.message_list_dict[target] = Message_list(
                    self.Message_box_frame)
            self.message_list = self.client.message_list_dict[target]
            self.message_list.show()

    def select_friend_request(self, dummyarg):
        """Set as target currently selected login on login list"""
        print('selected')
        target = self.friend_request_list.get(
            self.friend_request_list.curselection())
        print(target)
        if messagebox.askyesno('Add friend', 'Accept ' + target + '?'):
            self.client.acceptFriendRequest(target, True)
        else:
            self.client.rejectFriendRequest(target, False)
        self.update()

    def send_mess_event(self, dummyarg):
        # message = self.entry.get('1.0', tk.END)
        # self.client.chatTo(message=message)
        text = self.Mess.get(1.0, tk.END)
        if text != '\n':
            # message = 'msg;' + self.login + ';' + self.target + ';' + text[:-1]
            # print(text)
            self.client.chatTo(message=text[:-1])
            self.Mess.mark_set(tk.INSERT, 1.0)
            self.Mess.focus_set()
            self.Mess.delete(1.0, tk.END)
            return 'break'
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

    def add_event(self):
        if not (self.Search_entry['fg'] == 'lightgrey'):
            text = self.Search_entry.get()
            self.Search_entry.delete(0, END)
            if messagebox.askyesno('Add friend', 'Do you want to add ' + text):
                if self.client.addFriend(text):
                    messagebox.showinfo('Add friend', 'Sent')
                else:
                    messagebox.showwarning('Add friend', 'Failed!')

    def send_file_event(self, dymmarg):
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file")
        # print(filename)
        if filename is not None:
            try:
                self.client.sendFileTo(filename)
            except:
                return
        else:
            return
