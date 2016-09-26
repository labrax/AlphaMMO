# -*- coding: utf-8 -*-

"""
The constants for the server
"""

DATABASE_FILE = 'server.db'

# PERFORMANCE settings
SERVER_ITERATION_TIME = 1/60
PLAYER_PASS_THROUGH_OTHERS = True
#

# CONNECTION settings
HOST_BIND = ''
PORT_BIND = 1337
MAX_SERVER_CONN = 32
SOCKET_BUFFER = 4096
#

# SSL settings
CERTIFICATE_FILE = 'server.crt'
KEY_FILE = 'server.key'
#
