Name of the Application: InTouch

Creator: Alethea Tamanna Rangayya

Language Used: Python

Uses and Further Implementations:
By implementing login with work email addresses, the chatroom ensures secure access for authorized personnel. 
Within the chatroom, users can seamlessly share files, streamlining collaboration efforts. 
Communication over laptops without additional apps simplifies the process, enhancing user convenience. 
With network-only access and password activation, interactions remain secure within the organizational network. 
Furthermore, incorporating abuse detection mechanisms fosters a respectful environment, promoting productivity and well-being in the workplace.

About the system:
This project comprises essential files for establishing communication over a server.
In server.py, a socket object, which is our server, is instantiated, which binds itself to a specified host and port number (127.0.0.1 and 1234, respectively). 
This file contains functions for handling connections, receiving usernames, listening for all messages from clients, sending messages to individual clients, and broadcasting messages to all clients.

On the other hand, in client.py, another socket object is created to connect to the server's host IP address and port number. 
The graphical user interface (GUI) is created using the functionalities of Tkinter defined within this file.
It also contains functions for creating usernames (which can be autogenerated), receiving and sending messages between clients.

It's crucial to note that there's a client limit of 5 at any given time. 
Additionally, the concept of threads is employed to prevent infinite queues. 
This approach enables multiple operations to occur simultaneously within a single process, thereby enhancing system efficiency.