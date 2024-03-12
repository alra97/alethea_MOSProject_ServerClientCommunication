# import required modules
import sys
import string
import random
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

#Server Info
HOST = '127.0.0.1' #Server host address
PORT = 1234 #Server Port Number

#GUI PROPERTIES: FONTS
FONT=("Helvetica",17)
SMALL_FONT=("Helvetica",13)
BUTTON_FONT=("Helvetica",15)

#GUI PROPERTIES: COLORS
LIGHT_GREY='#E3E1D9'
DARK_BLUE='#1F2544'
LIGHT_GREEN='#CDFADB'
DARK_GREEN='#163020'
WHITE='#EEEADE'

#Creating a socket object 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Generating random usernames and inserting them in the username_textbox
def generate_username():
    username_textbox.delete(0, 'end')
    username_textbox.insert(0, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
    
#Inserting new messages on new lines
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

#Proccesses when the user clicks on the Leave button
def leave():
    messagebox.showerror("Leaving Chat", "Leaving chat now")
    print("Left Chat.")
    root.destroy()
    exit(0)
    
#Clears the textbox of any past input    
def clear_text():
    message_textbox.delete(0, 'end')

#On clicking the Join Button
def connect():
    #Connect to the server
    try:
        client.connect((HOST,PORT))
        print(f"Successfully Connected to the Server {HOST} {PORT}")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to Server", f"Unable to connect to server {HOST} {PORT}")

    print("Button Clicked")
    
    #Input username for the client
    username= username_textbox.get()
    print(username)
    if username != '':
        client.sendall(username.encode())
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
        generate_button.config(state=tk.DISABLED)
        message_textbox.config(state=tk.NORMAL)
        message_button.config(state=tk.NORMAL)
        leave_button.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Invalid Username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    
def send_message():
    #Function to send messages to the server
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, 'end')
    else:
        messagebox.showerror("Empty Message","Message Cannot be Empty")

#Creating a window that is not resizable  
root = tk.Tk()
root.geometry("800x800")
root.title("Messenger Client")
root.resizable(False, False) 

#Establishing grid view
root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=2)

#UI FRAMES
top_frame = tk.Frame(root, width=800, height=200, bg=DARK_GREEN)
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=800, height=400, bg=LIGHT_GREY)
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=800, height=100, bg=DARK_GREEN)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

#UI WIDGETS IN THE TOP FRAME
username_label = tk.Label(top_frame, text="Enter username: ", bg=DARK_GREEN,font=FONT, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=15)

username_textbox = tk.Entry(top_frame, font=FONT, bg= LIGHT_GREEN, fg=DARK_BLUE, width=13)
username_textbox.pack(side=tk.LEFT, padx=15)

generate_button = tk.Button(top_frame, text="Generate", font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, command=generate_username)
generate_button.pack(side=tk.LEFT, padx=15)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

#UI WIDGETS IN THE BOTTOM FRAME
message_textbox = tk.Entry(bottom_frame, font=FONT, bg= LIGHT_GREEN, fg=DARK_BLUE, width=30)
message_textbox.pack(side=tk.LEFT,padx=15)
message_textbox.config(state=tk.DISABLED)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, command=send_message)
message_button.pack(side=tk.LEFT, padx=15)
message_button.config(state=tk.DISABLED)

leave_button = tk.Button(bottom_frame, text="Leave", font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, command=leave)
leave_button.pack(side=tk.LEFT, padx=15)
leave_button.config(state=tk.DISABLED)

#UI WIDGET IN THE MIDDLE FRAME
message_box =scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, width=67, height=29.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

#Function to receive messages from the server
def listen_for_messages_from_server(client):

    while 1:

        message= client.recv(2048).decode('utf-8')
        if message != '':
            #splits the message into the format followed, example alethea:hi
            username= message.split(":")[0]
            content= message.split(":")[1]
            add_message(f"[{username}] : {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

#main function
def main():
    
    root.mainloop() #start the window

#run it directly from client.py only
if __name__ == '__main__':
    main()