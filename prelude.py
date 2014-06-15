import os,sys,time,traceback as tb,re,json
from pprint import pprint
data = ''.join(sys.stdin.xreadlines())
def get_tuple(cursor, name, tup, skip_ws=True):
    if skip_ws:  ws,cursor = get_ws(cursor)
    ret = {}
    cursor0 = ret['start'] = cursor
    while data.startswith(tup, cursor):
        cursor += 1
        pass
    ret['tok']=data[cursor0:cursor]
    if not ret['tok']:
        ret['err'] = 'not found'
    return ret,cursor
def get_ws(cursor):
    ret = {}
    cursor0 = ret['start'] = cursor
    while data.startswith(tuple(' \t\r\n\v'),cursor):
        cursor += 1
        pass
    ret['ws']=data[cursor0:cursor]
    return ret,cursor
def get_id(cursor, skip_ws=True):
    return get_tuple(cursor, 'id',
                     tuple('abcdefghijklmnopqrstuvwxyz'+
                           'ABCDEFGHIJKLMNOPQRSTUVWXYX'+
                           '0123456789_'), skip_ws=skip_ws)
def get_int(cursor, skip_ws=True):
    return get_tuple(cursor, 'int',
                     tuple('0123456789'))
def get_xstr(cursor, tok_str, skip_ws=True):
    if skip_ws:  x,cursor = get_ws(cursor)
    ret = {}
    cursor0 = ret['start'] = cursor
    if data.startswith(tok_str, cursor):
        cursor += len(tok_str)
        pass
    ret['str']=data[cursor0:cursor]
    if not ret['str']:
        ret['err'] = 'not found'
    return ret,cursor
def get_str_url_encoded(cursor,skip_ws=True):
    from urllib import unquote
    if skip_ws:  x,cursor = get_ws(cursor)
    cursor0=cursor
    if not data.startswith('"',cursor):
        return dict(err='not found'), cursor
    n = data.find('"',cursor+1)
    if n == -1:
        return ('unbound string',''),cursor
    ret = {}
    ret['start']=cursor0
    ret['str'] = unquote(data[cursor+1:n])
    return ret,n+1
get_str_url=get_str_url_encoded
