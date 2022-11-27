import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import threading
from tkinter import filedialog
from tkinter import messagebox
# from PIL import ImageTk, Image

#screen resolution
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550

color = ["#07080C", "#8B7E74", "#C7BCA1", "#F1D3B3"]

# image = Image.open("background.png")


class Message_list:
    def __init__(self, frame):
        #self.messages_list = scrolledtext.ScrolledText(frame, wrap='word', font=('Helvetica', 13))
        #self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        #self.messages_list.configure(state='disabled')
        #frame.grid_rowconfigure(0, weight=1)
        #frame.grid_columnconfigure(0, weight=1)
        self.messages_list = scrolledtext.ScrolledText(frame, wrap='word')
        #self.Message_box.grid(row=0,column=0,sticky='nswe')
        self.messages_list.insert(END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')

    def write(self, text):
        print(text)
        self.messages_list.configure(state='normal')
        if text != '\n':
            self.messages_list.insert(tk.END, text)
        self.messages_list.configure(state='disabled')
        self.messages_list.see(tk.END)

    def show(self):
        print("show")
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)

    def hide(self):
        print('hide')
        self.messages_list.pack_forget()


class Window(object):
    def __init__(self, title, font, client):
        self.title = title
        self.closewindow = False
        self.font = font
        self.client = client
        self.root = tk.Tk()
        # self.background_image = ImageTk.PhotoImage(image=image)
        self.root.config(bg=color[0])
        self.root.title(title)
        self.build_window()


class LoginWindow(Window):
    def __init__(self, client, font):
        super(LoginWindow, self).__init__(
            'Chat application: Login', font, client)
        self.build_window()

    def build_window(self):
        ## configure window
        #set coordinate
        coor_x = int((self.root.winfo_screenwidth()-SCREEN_WIDTH)/2)
        coor_y = int((self.root.winfo_screenheight() - SCREEN_HEIGHT)/2)
        self.root.geometry('%dx%d+%d+%d' %
                           (SCREEN_WIDTH, SCREEN_HEIGHT, coor_x, coor_y))
        self.root.minsize(400, 350)
        #add background image
        background_label = Label(self.root)
        # background_label.config(image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # create frames
        upper_frame = Frame(self.root,bg=color[0])
        upper_frame.grid(row=0, column=0)
        middle_frame = Frame(self.root, bg=color[0])
        middle_frame.grid(row=1, column=0)
        bottom_frame = Frame(self.root, bg=color[0])
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
        
        tk.Label(upper_frame,text="Welcome to Group 13 Chat application", font=('Arial',28),fg='#FFFFFF',bg=color[0]).grid(row=0,column=0)
        tk.Label(upper_frame,text="Login or register to start chats with friend!", font=self.font,fg='#FFFFFF',bg=color[0]).grid(row=1,column=0)
        
        
        # username label and text entry box
        tk.Label(middle_frame, text="User Name", font=self.font, fg=color[3], bg=color[0]).grid(
            row=0, column=0, padx=20, pady=20, sticky='e')
        self.username_input = tk.Entry(
            middle_frame, font=self.font, bg=color[3], fg=color[2])
        self.username_input.grid(row=0, column=1, sticky='w', padx=20)
        self.username_input.focus_set()
        # password label and password entry box
        Label(middle_frame, text="Password", font=self.font, fg=color[3], bg=color[0]).grid(
            row=1, column=0, padx=20, pady=20, sticky='e')
        self.password_input = Entry(
            middle_frame, font=self.font, show='*', bg=color[3], fg=color[2])
        self.password_input.grid(row=1, column=1, sticky='e', padx=20)

        # IP_inp= tk.Label(middle_frame,text="IP",font=self.font) #.grid(row=2, column=0,padx=10,sticky='e')
        # self.IP_input = tk.Entry(middle_frame, font=self.font)
        # button
        Button(bottom_frame, text="Login", command=self.Login, font=self.font,
               fg=color[1], bg=color[3]).grid(row=0, column=1, padx=40, pady=10)
        Button(bottom_frame, text="Register", command=lambda: [self.killbutton(bottom_frame), self.add_register(
        )], font=self.font, fg=color[1], bg=color[3]).grid(row=0, column=0, padx=40, pady=10)

    def killbutton(self, frame):
        for widget in frame.grid_slaves():
            widget.destroy()

    def add_register(self):
        # IP_inp.grid(row=2, column=0,padx=10,sticky='e')
        # self.IP_input.grid(row=2, column=1,sticky='w')
        bottom_frame2 = Frame(self.root)
        bottom_frame2.grid(row=2, column=0)
        Button(bottom_frame2, text="Confirm registration", command=self.Register,
               font=self.font, fg=color[3], bg=color[1]).grid(row=0, column=0)

    def Register(self):
        self.client.Connect()
        # self.add_resgister(middle_frame)
        username = self.username_input.get()
        password = self.password_input.get()
        # Got verified result from server
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

        # Got verified result from server
        if not self.client.Login(username, password):
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
        self.closewindow = True
        self.root.quit()


class ChatWindow(Window):
    def __init__(self, client, font):
        super(ChatWindow, self).__init__(
            'Chat application: Chat Window', font, client)
        self.build_window()
        self.update()
        self.bool = True

    def showFriend_event(self, event):
        print(("showFriend_event"))
        self.Chat_button.pack_forget()
        self.Show_button_label.pack(side=LEFT, fill=X, expand=YES)
        self.Friend_request_button_label.pack_forget()
        self.Friend_request_button.pack(side=LEFT, fill=X, expand=YES)
        self.update()
        self.friend_request_list.pack_forget()
        self.logins_list.pack(side=LEFT, fill=BOTH, expand=YES)

    def Friend_request_event(self, event):
        print("friend_request_event")
        self.Show_button_label.pack_forget()
        self.Chat_button.pack(side=LEFT, fill=X, expand=YES)
        self.Friend_request_button.pack_forget()
        self.Friend_request_button_label.pack(side=LEFT, fill=X, expand=YES)
        self.update()
        self.logins_list.pack_forget()
        self.friend_request_list.pack(side=LEFT, fill=BOTH, expand=YES)

    def build_window(self):
        """Build chat window, set widgets positioning and event bindings"""
        # Size config
        coor_x = int((self.root.winfo_screenwidth()-SCREEN_WIDTH)/2)
        coor_y = int((self.root.winfo_screenheight() - SCREEN_HEIGHT)/2)
        self.root.geometry('%dx%d+%d+%d' %
                           (SCREEN_WIDTH, SCREEN_HEIGHT, coor_x, coor_y))
        self.root.minsize(600, 400)

        # create all of the main containers
        self.header = Frame(self.root,bg=color[0])
        self.body = Frame(self.root,bg=color[0])
        self.left_frame = Frame(self.body,bg=color[0])
        self.right_frame = Frame(self.body,bg=color[0])

        # layout all of the main containers
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=8)
        self.root.grid_columnconfigure(0,weight=1)
        self.header.grid_columnconfigure(0,weight=1)
        self.header.grid_rowconfigure(0,weight=1)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0,weight=1)

        self.header.grid(row=0, column=0,sticky='nsew')
        self.body.grid(row=1, column=0,sticky='nsew')

        self.left_frame.grid(row=0, column=0,sticky='nsew')
        self.right_frame.grid(row=0, column=1,sticky='nsew')

        #header components
        self.Username_label = Label(self.header, text="Welcome, " + self.client.username, font=('Arial', 20),bg=color[0],fg="#FFFFFF")
        self.Username_label.grid(row=0,column=0,sticky='w')

        # create all of the left containers
        self.Search_Frame = Frame(self.left_frame, bg=color[0])
        self.Search_Frame.grid_rowconfigure(0, weight=1)
        self.Search_Frame.grid_columnconfigure(0, weight=1)
        self.Search_entry = Entry(self.Search_Frame,font=self.font,fg=color[1])
        self.Search_entry.insert(0,'Type people\'s name here')
        self.Search_entry.bind('<FocusIn>',self.temp_text)
        # self.Search_entry.bind('<Return>', self.add_event)
        self.Search_entry.grid(row=0, column=0,sticky='nsew')
        findbutton=Button(self.Search_Frame,text='Find',command=self.add_event,font=self.font,fg=color[1],bg=color[3])
        findbutton.grid(row=0,column=1)
        
        self.Lists_Frame = Frame(
            self.left_frame, bg=color[0], pady=3)
        self.Chat_button = Button(self.Lists_Frame, text='Chats',font=self.font,fg=color[3],bg=color[1])
        self.Chat_button.bind('<Button-1>', self.showFriend_event)
        self.Show_button_label = Label(
            self.Lists_Frame, text='Chats',font=self.font,fg=color[1],bg=color[3])

        self.Friend_request_button = Button(
            self.Lists_Frame, text='Friend requests',font=self.font,fg=color[3],bg=color[1])
        self.Friend_request_button.bind(
            '<Button-1>', self.Friend_request_event)
        self.Friend_request_button_label = Label(
            self.Lists_Frame, text='Friend requests',font=self.font,fg=color[1],bg=color[3])

        self.Show_button_label.pack(side=LEFT, fill=X, expand=YES)
        self.Friend_request_button.pack(side=LEFT, fill=X, expand=YES)

        self.logins_list_Frame = Frame(self.left_frame, bg=color[0], pady=3)
        self.logins_list_Frame.grid_rowconfigure(0, weight=1)
        self.logins_list_Frame.grid_columnconfigure(0, weight=1)
        self.logins_list = Listbox(
            self.logins_list_Frame, selectmode=SINGLE, exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)
        self.logins_list.pack(side=LEFT, fill=BOTH, expand=YES)

        self.friend_request_list = Listbox(
            self.logins_list_Frame, selectmode=SINGLE, exportselection=False)
        self.friend_request_list.bind(
            '<<ListboxSelect>>', self.select_friend_request)
        #self.friend_request_list.pack(side=LEFT, fill=BOTH, expand=YES)

        self.Search_Frame.grid(row=0, column=0,sticky='nsew')
        self.Lists_Frame.grid(row=2, column=0,sticky='nsew')
        self.logins_list_Frame.grid(row=3, column=0,sticky='nsew')

        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # create all of the right containers
        self.Target_name_frame = Frame(self.right_frame, bg=color[3], pady=3)
        self.Target_name_frame.grid_rowconfigure(0, weight=1)
        self.Target_name_frame.grid_columnconfigure(0, weight=1)
        self.Target = Label(self.Target_name_frame,
                            text='Choose a friend to chat')
        self.Target.grid(row=0, column=0, sticky='nswe')

        self.Message_box_frame = Frame(self.right_frame, bg='black', pady=3)
        self.message_list = Message_list(self.Message_box_frame)
        self.message_list.show()

        self.Entry_frame = Frame(
            self.right_frame, bg='grey', height=100, pady=3)
        self.Entry_frame.grid_rowconfigure(0, weight=1)
        self.Entry_frame.grid_columnconfigure(0, weight=1)
        self.Entry = Text(self.Entry_frame)
        self.Entry.bind('<Return>', self.send_entry_event)
        self.Entry.grid(row=0, column=0,sticky='nsew')

        self.Send_file_button = Button(self.right_frame, text='Send file')
        self.Send_file_button.bind('<Button-1>', self.send_file_event)
        self.Send_file_button.grid(row=3, column=0,sticky='nsew')

        self.Target_name_frame.grid(row=0, column=0,sticky='nsew')
        self.Message_box_frame.grid(row=1, column=0,sticky='nsew')
        self.Entry_frame.grid(row=2, column=0,sticky='nsew')

        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=4)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    ##mini functions
    def temp_text(self,dummyarg):
        self.Search_entry.delete(0, END)
        self.Search_entry.configure(fg="#000000")       
    
    ##main
    def run(self):
        """Handle chat window actions"""
        self.root.mainloop()

    def update(self):
        print("Update friend list")
        # show friend list in chat tab
        friendlist = self.client.showFriend()
        self.logins_list.delete(0, 'end')
        self.friend_request_list.delete(0, 'end')
        for friend in friendlist:
            if friendlist[friend] == False:
                # print(friend)
                status = "offline"
            if friendlist[friend] == True:
                status = "online"
            self.logins_list.insert(tk.END, friend + ': ' + status)

        # show friend request list in friend requests tab
        friendlist = self.client.showFriendRequest()
        for friend in friendlist:
            self.friend_request_list.insert(tk.END, friend)

    def on_close(self):
        self.client.close()
        print('Close window')
        self.root.destroy()

    def selected_login_event(self, event):
        """Set as target currently selected login on login list"""
        cursor = self.logins_list.get(self.logins_list.curselection())
        target = cursor.split(':')[0]
        status = cursor.split(':')[1][1:]

        # if target is None:
        #     return

        self.Target.config(text=target)
        self.client.target = target
        self.message_list.hide()
        # if target is None:
        #     return

        if status == 'online':
            if target not in self.client.buff_dict:
                self.client.startChatTo(target)
            elif not self.client.buff_dict[target].status:
                self.client.startChatTo(target)
        else:
            if target not in self.client.message_list_dict:
                self.client.message_list_dict[target] = Message_list(
                    self.Message_box_frame)

        self.message_list = self.client.message_list_dict[target]
        self.message_list.show()

    def select_friend_request(self, event):
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

    def send_entry_event(self, event):
        #message = self.entry.get('1.0', tk.END)
        #self.client.chatTo(message=message)
        text = self.Entry.get(1.0, tk.END)
        if text != '\n':
            #message = 'msg;' + self.login + ';' + self.target + ';' + text[:-1]
            print(text)
            self.client.chatTo(message=text[:-1])
            self.Entry.mark_set(tk.INSERT, 1.0)
            self.Entry.focus_set()
            self.Entry.delete(1.0, tk.END)
            return 'break'
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

    def add_event(self):
        text = self.Search_entry.get()
        self.Search_entry.delete(0, END)
        if messagebox.askyesno('Add friend', 'Do you want to add ' + text):
            if self.client.addFriend(text):
                messagebox.showinfo('Add friend', 'Sent')
            else:
                messagebox.showwarning('Add friend', 'Failed!')

    def send_file_event(self, event):
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file")
        print(filename)
        if filename is not None:
            try:
                self.client.sendFileTo(filename)
            except:
                return
