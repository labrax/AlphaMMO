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