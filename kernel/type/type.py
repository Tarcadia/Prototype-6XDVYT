
# -*- coding: UTF-8 -*-



# ID := str isidentifier && isascii && len==64

def is_id(id:str) -> bool:
    return id.isidentifier() and id.isascii() and len(id) == 64



# CALL := str isidentifier && isascii

def is_call(call:str) -> bool:
    return isinstance(call, str) and call.isidentifier() and id.isascii()



# PARAMS := str

def is_params(params:str):
    return isinstance(params, str)



# MESSAGE := (ID, CALL, PARAMS)

def is_message(message:tuple):
    return isinstance(message, tuple) and len(message) == 3 and is_id(message[0]) and is_call(message[1]) and is_params(message[2])
