# Python program to translate
# speech to text and text to speech
import socket
import speech_recognition as sr
import sys
import PyQt5.QtWidgets
import startlogo


def __init__():
    pass


def start_open_screen(server_socket):
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    ex = startlogo.Ui_MainWindow()
    w = PyQt5.QtWidgets.QMainWindow()
    ex.setupUi(w, server_socket)
    w.show()
    app.exec()


def sign_up(server_socket):
    firstname = input("enter your first name")
    lastname = input("enter your last name")
    client_name = input("enter username")
    server_socket.send(("username:" + client_name).encode())
    data1 = server_socket.recv(1024).decode()
    print(data1)
    while "taken" in data1:
        client_name = input("username taken, enter  new username")
        server_socket.send(("username:" + client_name).encode())
        data1 = server_socket.recv(1024).decode()
    password1 = input("enter password")
    userInfo = client_name + " " + firstname + " " + lastname + " " + password1
    server_socket.send(userInfo.encode())
    data1 = server_socket.recv(1024).decode()
    print(data1)


def get_button_data(button1, button2, ssocket):
    button1.clicked.connect(sign_up, args=(ssocket,))


def voice_to_text():
    global MyText
    r = sr.Recognizer()
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


ans = " "
closeFunc = False
MyText = ""
counterOfText = 0
buf = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8820))
start_open_screen(s)

name = input("enter username")
s.send(("usernameold:" + name).encode())
data = s.recv(1024).decode()

while "found." in data:
    name = input("user not found, enter  new username")
    s.send(("username:" + name).encode())
    data = s.recv(1024).decode()
password = input("enter password")
s.send(("password:" + password).encode())
data = s.recv(1024).decode()
while "wrong:" in data:
    password = input("password is wrong, re-enter password")
    s.send(("password:" + password).encode())
    data = s.recv(1024).decode()
    print(data)
ready = input("press any key to start, press q to quit")
if "q" in ready:
    ready = "q:"
while "q:" not in ready:
    s.send("ready: indeed".encode())
    data = s.recv(1024).decode()
    print(data)
    while "The letter" not in data:
        data = s.recv(1024).decode()
        print(data)
    ans = " "
    while "finished:" not in ans:
        print(ans)
        MyText = " "
        voice_to_text()
        s.send(MyText.encode())
        ans = s.recv(buf).decode()

    print(ans)
    s.send("game done:".encode())
    ready = input("press any key to start, press q to quit")
    if "q" in ready:
        ready = "q:"
