# Import required modules
import socket #main communication
import threading #concurrent threading

HOST = '127.0.0.1' #IPv4 address of server
PORT = 1234 #can be any(0-65535)
CLIENT_LIMIT = 5 #Maximum 5 clients can connect at the SAME TIME
active_clients = [] #List of all currently active users

#Function to listen for any upcoming messages from a client
def listen_for_messages(client,username):
    
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg= username + ':' + message
            send_message_to_all(final_msg)

        else:
            #If message from the client remains null, 
            # client has left the server.
            leave_user= "SERVER: "+ f"{username} left the chat."
            active_clients.remove((username,client))
            send_message_to_all(leave_user)
            pass
  
#Function to send any new message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

#Function to send any new message to all the clients are 
#currently connected to the server
def send_message_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

#Function to handle client
def client_handler(client):
    
    #Server will listen for client message that will 
    #contain the username
    while 1:
        #2048 Maximum Size of the message
        username= client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            new_user= "SERVER: "+ f"{username} joined the chat."
            send_message_to_all(new_user)
            break
        else:
            #print("Client username is empty")
            pass

    threading.Thread(target=listen_for_messages(client, username)).start()
    #threading.Thread(target=check_users(client)).start()

#Main function
def main():
    #Creating the socket class object
    #AF_INET: IPv4 Addresses
    #SOCK_STREAM: TCP packets for communication
    #SOCK_DGRAM: UDP packets for communication
    server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Creating a try-catch block
    try:
        #Provide the server with an address in the form of 
        #host IP and port
        server.bind((HOST,PORT))
        print(f"Running the Server on {HOST} {PORT}")
    except: 
        print(f"Unable to bind to host {HOST} and port {PORT}")

    #Set server limit
    server.listen(CLIENT_LIMIT)

    #This while loop will keep listening to client connections
    while 1:
        #Client refers to the socket of the client
        #Address refers to the client details such as IP Addresses, ports
        client, address = server.accept()
        print(f"Successfully Connected to Client {address[0]} {address[1]}")

        #Using threading concurrently
        threading.Thread(target=client_handler, args=(client,)).start()

#run it directly from server.py only
if __name__ == '__main__':
    main()
    
