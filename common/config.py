"""
Configuration module for app

Stores the global variables used for connection, for encoding settings and a customize print function.
"""
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
HEADER_SIZE = 20
FORMAT = 'utf-8'

def print_log(source, message):
    print(f"[{source}] {message}")