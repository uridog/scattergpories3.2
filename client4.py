# Python program to translate
# speech to text and text to speech
import hashlib
import hmac
import socket
import ssl

import speech_recognition as sr

context = ssl.create_default_context()

# Set the context to not verify the server's SSL/TLS certificate
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def calc_digest(key, message):
    key = bytes(key, 'utf-8')
    message = bytes(message, 'utf-8')
    dig = hmac.new(key, message, hashlib.sha256)
    return dig.hexdigest()


def create_msg(data_to_send):
    data_len = len(data_to_send)
    data_len_len = len(str(data_len))
    data_len = str(data_len)
    for i in range(4 - data_len_len):
        data_len = "0" + data_len
    hmac_data = calc_digest("banana", data_to_send)
    return hmac_data + data_len + data_to_send


def handle_msg(client_socket):
    hmac_received = client_socket.recv(64).decode()
    data_len_received = client_socket.recv(4).decode()
    data_received = client_socket.recv(int(data_len_received)).decode()
    if calc_digest("banana", data_received) != hmac_received:
        return "!"
    return data_received


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
s = context.wrap_socket(s, server_hostname='127.0.0.1')
signUpOrLogIn = input("type-0 to sign up \n type-1 to log in")
if signUpOrLogIn == "0":
    firstname = input("enter your first name")
    lastname = input("enter your last name")
    name = input("enter username")
    s.send(("username:" + name).encode())
    data = s.recv(1024).decode()
    print(data)
    while "taken" in data:
        name = input("username taken, enter  new username")
        s.send(("username:" + name).encode())
        data = s.recv(1024).decode()
    password = input("enter password")
    userInfo = name + " " + firstname + " " + lastname + " " + password
    s.send(userInfo.encode())
    data = s.recv(1024).decode()
    print(data)
elif signUpOrLogIn == "1":
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
