# AlphaMMO

This is the implementation of my undergraduate project.


## Running it

Be sure that the client and server are using the same version of Stackless Python interpreter (or at least pickle version). I recommend version 3.4.

-> Install required packages:
'''
sudo apt-get install libssl-dev openssl libfreetype6-dev
sudo apt-get install build-essential zlib1g-dev (or zlib-devel)
sudo apt-get install libreadline-dev
sudo apt-get build-dep python 2.7
'''
-> Download Stackless from https://bitbucket.org/stackless-dev/stackless/wiki/Download
-> Configure and compile Stackless
'''
./configure --prefix=/opt/stackless --enable-unicode=ucs4
make
sudo make install
'''
-> Install packages on Stackless:
'''
stackless -m pip install pygame pickle pyopenssl sqlite3 stackless-python
'''

If you use Stackless Python 2.7 you'll need to install more packages:
'''
stackless -m pip install enum34
'''

On Windows you'll need to:
-> Install vcpython: http://aka.ms/vcpython27
-> Install get-pip: https://bootstrap.pypa.io/get-pip.py


PyGame might required that you install dependencies:
-> Check http://www.pygame.org/wiki/CompileUbuntu.
-> And install:
'''
sudo python3 -m pip install hg+http://bitbucket.org/pygame/pygame
'''


If you want to access the database:
'''
sudo apt-get install libsqlite3-dev sqlite3 sqlitebrowser
'''


## Why stackless?

Stackless is an optimized interpreter for Python.
It uses less memory, it is faster and simpler. Tasklets are simple to use and has the paradigm of parallelization with many-to-one threads (check many-to-one in the O.S. book from Silberschatz 9th edition). 


Pros:
- Simple way to implement "threads": you must use stackless.schedule() when passing over the use of the CPU, if you do not then you will not have the "parallelism".
- Optimized interpreter.


Cons:
- It is not a true parallelism.
- Requires another Python interpreter (the one from stackless).

We use on the server a tasklet for each entity (player and NPC), and in the client for the most important components: communication and main loop.


## How is the game implemented?

It uses an Model-View-Controller approach. Components send message to each other (to do this is used the observer pattern!) as required by our logic. We have components of socket communication, game states, drawing states and main loop (not all of them are entirely independent) and on the server we have one tasklet (as a "component") for each entity.
Some of the sequences of iteractions are:

Player --> <INPUT> --> Server
Server --> <EVERYTHING THAT OCCURS> --> Client
Client States --> <EVERYTHING DRAWABLE> --> Client Screen


## Generating the server certificate

Follow this sequence of commands on Bash::
'''
openssl genrsa -des3 -out server.orig.key 2048
openssl rsa -in server.orig.key -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
'''
Be sure to add the files on both server and client.


## How is the communication between the components and client-server communication?

The components communication in the client are at: src/util/alpha_protocol.py

The socket communication protocol is at: src/util/alpha_socket_comm.py


## What is the database used for?

It is used solely for the purpose of login (at the present stage), check it at: src/server_util/server_database.py
We store a salt and the hashed password using the salt, this way we improve the security of the password in case the database is stolen.


## How is the TCP message send?

First we get the length of the message. We send it as a text followed by a space, and in the following the message.

'''python
def send_message(msg):
    will_be_send = str(len(msg)) + ' ' + str(msg)
    return socket.send(will_be_send)
'''

So, what do we actually do?
First we dump the object as a pickle serialized object, that is our 'msg'. We decode to a byte sequence as we do it with the length of the message, we send it using the same schema with the delimiter.


## What can be improved?

-> More content should be added, the player can't interact properly with the game.
-> SSL should be used only for authentication, and an unique use code should then be used, with a CRC and a sequence number to maintain that only the proper user (and not an intrusor) is playing under a non-ssl socket. SSL is slow for a game that demands low-latency multiple messages.
-> The protocol should be re-planned to avoid the sending of multiple messages "repeated" with only the information of a single entity, it should be waited for bigger packages to avoid TCP/SSL slowdown (but not too long for the game not to be laggy).
-> PyGame rendering is slow. pyopengl should run smother on Windows.


## Other TO-DOs:

"Simpler ones":
- separate hair from the helmet itens
- other windows (player itens, backpack, text and status)
- itens id
- itens on the floor
- players movement (and invalid pos)

Bugs:
- way too many checks for npcs movement (insert time.time() for checks)
- slow rendering on windows (pygame to pyopengl drawing)

Problems:
- text is on a lazy approach

Future:
- interaction: such as attack, picking items
- server's ai: aggresive NPCs, NPCs dieing and reseting
- internal GUI: player items, 't' to write and send a text; draw player hp and mp
- external GUI: message ui popup for server status and other client messages
- actionable scripts (on position, etc), and event messages to screen
- character attributes and storing it on the database (as a pickle serialization maybe?)
- character list
- movement changing order of checks for movement: insted of setting after complete movement set before (and only notify the client later - dirty fix)
- invalid ip makes the client retry connection indefinitely
- SSL wrong version number

One possibility:
- different skills and characters (as in KAG)
- itens not as a priority
- mouse targets
- semi-random map or arena
- minimap maybe
- ia

Maybe:
- remove stackless from client


## References:

Some references for the project.

-> http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
-> https://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate
-> https://www.cigital.com/blog/python-pickling/


Python documentation:

-> https://docs.python.org/3/library/socket.html
-> https://docs.python.org/3/library/ssl.html
-> https://docs.python.org/3/library/pickle.html

