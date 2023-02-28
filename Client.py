#region Libraries

import socket
import threading
import pyaudio
from tkinter import *
import tkinter.messagebox
import sys
import win32api
import win32gui

#endregion

#region Mute Script

def mute(event = ''):
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

#endregion

#region Connected

def connected(ip, port, nickname):
    connectedGUI = Tk()
    connectedGUI.title("Lessy - Voice Chat")
    connectedGUI.geometry("158x143+380+320")
    connectedGUI.resizable(False, False)
    connectedGUI.configure(bg = "black")
    connectedGUI.bind('<Caps_Lock>',mute)

    serverLabel = Label(connectedGUI, text="{}:{}".format(ip, port), fg = "red", bg = "black")
    serverLabel.place(x = 5, y = 5)
    nicknameLabel = Label(connectedGUI, text="{}".format(nickname), fg = "red", bg = "black")
    nicknameLabel.place(x=5,y=115)

    muteButton = Button(connectedGUI, width=5, text="Mute", bg="black", fg="red", command = mute)
    muteButton.pack()
    muteButton.place(x=61, y=60)
    connectedGUI.mainloop()

#endregion

#region Connect Function

def connect(server,port,nickname,password):
    SERVER = server
    PORT = port
    PORT = int(PORT)
    PASSWORD = password
    if PASSWORD == "Password": # Set this line whatever you want to use for password!
        mainGUI.destroy()
        threadPanelThread = threading.Thread(target = connected,args=(SERVER, PORT, nickname))
        threadPanelThread.start()
        p = pyaudio.PyAudio()
        client = socket.socket()
        client.connect((SERVER, PORT))
        Format = pyaudio.paInt16
        Chunks = 48
        Channels = 1
        Rate = 21000

        input_stream = p.open(format = Format,
            channels = Channels,
            rate = Rate,
            input = True,
            frames_per_buffer = Chunks)

        output_stream = p.open(format = Format,
            channels = Channels,
            rate = Rate,
            output = True,
            frames_per_buffer = Chunks)

        def send():
            while True:
                try:
                    data = input_stream.read(Chunks)
                    client.send(data)
                except:
                    break

        def receive():
            while True:
                try:
                    data = client.recv(Chunks)
                    output_stream.write(data)
                except:
                    break

        t1 = threading.Thread(target = send)
        t2 = threading.Thread(target = receive)
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        input_stream.close()
        output_stream.close()
        p.terminate()
    else:
        tkinter.messagebox.showerror(title = "Connection Failed!", message = "Connection Failed!")

def quit():
    sys.exit(0)

#endregion

#region First Gui

if __name__ == "__main__":
    mainGUI = Tk()
    mainGUI.title("Connect")
    mainGUI.geometry("358x143+780+420")
    mainGUI.resizable(False, False)
    mainGUI.configure(background="black")
    mainGUI.bind("<Return>", lambda x: connect(serverEntry.get(), portEntry.get(), nicknameEntry.get(), passwordEntry.get()), mainGUI)
    # ServerLabel
    serverLabel = Label(mainGUI,text = "Ip adress:",fg="red",bg="black")
    serverLabel.place(x = 18, y = 5)
    # ServerEntry
    serverEntry = Entry(mainGUI, width = 34, fg = "red", borderwidth = 1, relief = "solid")
    serverEntry.pack(side = RIGHT)
    serverEntry.place(x = 20, y = 30)
    serverEntry.focus()
    # PortLabel
    portLabel = Label(mainGUI, text = "Port:", fg="red",bg="black")
    portLabel.place(x = 240, y = 5)
    # PortEntry
    portEntry = Entry(mainGUI, width = 15, fg = "red", borderwidth = 1, relief = "solid")
    portEntry.pack()
    portEntry.place(x = 242, y = 30)
    # NicknameLabel
    nicknameLabel = Label(mainGUI, text = "Nickname:",fg="red",bg="black")
    nicknameLabel.place(x = 18, y = 55)
    # NicknameEntry
    nicknameEntry = Entry(mainGUI, width=34, fg = "red", borderwidth = 1, relief = "solid")
    nicknameEntry.pack(side = RIGHT)
    nicknameEntry.place(x = 20, y = 80)
    # PasswordLabel
    passwordLabel = Label(mainGUI, text = "Password:",fg="red",bg="black")
    passwordLabel.place(x = 240,y = 55)
    # PasswordEntry
    passwordEntry = Entry(mainGUI, width=15, fg = "red", borderwidth = 1, relief = "solid")
    passwordEntry.pack()
    passwordEntry.place(x = 242, y = 80)
    # ConnectButton
    connectButton = Button(mainGUI, width=7, text = "Connect", bg="black",fg="red",borderwidth = 1, relief = "solid",command = lambda: connect(serverEntry.get(), portEntry.get(), nicknameEntry.get(), passwordEntry.get()))
    connectButton.pack()
    connectButton.place(x = 155, y = 110)
    mainGUI.mainloop()

#endregion
