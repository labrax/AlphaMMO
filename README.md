# AlphaMMO
Documentation in portuguese

https://docs.google.com/document/d/1YKFzcyDTlr9NVw1qT3qqO1lUdW8CVSUJtSND6V8TuUU/edit?usp=sharing


Notes:
-------------------------------------------------------------------
FLOW:
  PLAYER =inputs> SERVER
  SERVER =everything> STATES
  STATES =everything> SCREEN

AlphaCommunication:
  player_input ---out_destination is--> server.notify

  server ---in_destination--> client_states.notify

Protocol:
  MOVE
  MAP: TILES...
-------------------------------------------------------------------

- table index - ok
- entity name - ok
- display entity name/text - ok
- server_database - ok

- server ssl / socket and protocol - message passing

References:
-------------------------------------------------------------------
http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
https://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate
https://www.cigital.com/blog/python-pickling/

https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/ssl.html
https://docs.python.org/3/library/pickle.html
-------------------------------------------------------------------

- separate hair from the helmet itens
- other windows (player itens, backpack, text and status)
- itens id
- itens on the floor
- players movement (and invalid pos)

bugs:
- way too many checks for npcs movement (insert time.time() for checks)

problems:
- text is on a lazy approach

future:
- server's ai
- actionable scripts (on position, etc)