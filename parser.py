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
    ret['name']=name
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
def get_str(cursor, name, tok_str=None, skip_ws=True):
    tok_str = tok_str or name
    if skip_ws:  x,cursor = get_ws(cursor)
    
    ret = {}
    cursor0 = ret['start'] = cursor
    ret['type']=name
    ret[ name ]=True
    if data.startswith(tok_str, cursor):
        cursor += len(tok_str)
        pass
    ret['str']=data[cursor0:cursor]
    if not ret['str']:
        ret['err'] = 'not found'
    return ret,cursor
def get_list(cursor, type, func):
    arr = []
    cursor0 = cursor
    while 1:
        ret2,cursor = func(cursor)
        if 'err' in ret2:
            ret = {}
            ret['start']=cursor0
            #ret['list']=arr
            ret[type]=arr
            return ret,cursor
        arr.append(ret2)
        pass
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

def get_term(c):
    r0={"start":c};c0=c

    r, c = get_id(c)
    if 'err' not in r:
        if 0: r0['label']=r;   r0['finish']=c; return r0, c
        else : r['label']=True; r['finish']=c; return r, c

    r, c = get_str_url_encoded(c)
    if 'err' not in r:
        if 0: r0['xstr']=r;   r0['finish']=c; return r0, c
        else : r['xstr']=True; r['finish']=c; return r, c

    r, c = get_str(c,"null","null")
    if 'err' not in r:
        if 0: r0['null']=r;   r0['finish']=c; return r0, c
        else : r['null']=True; r['finish']=c; return r, c

    r['err'] = "No matches"
    return r, c0

def get_nterm(c):
    r0={"start":c};c0=c

    r, c = get_id(c)
    if 'err' in r:
        return r, c
    r0['name'] = r

    r, c = get_str(c,"s1",":")
    if 'err' in r:
        return r, c
    r0['s1'] = r

    r, c = get_str(c,"s2",":")
    if 'err' in r:
        return r, c
    r0['s2'] = r

    r, c = get_term(c)
    if 'err' in r:
        return r, c
    r0['term'] = r

    r0['finish'] = c
    return r0, c

def get_nterms(c):
    r0={ "start":c, "nterms":[] }; c0=c
    while 1:
        sub=[]

        r, c = get_nterm(c)
        if 'err' in r: r0['finish']=c; return r0, c0
        sub.append(r)

        c0=c; r0['nterms'].extend(sub)
        pass
    pass

def get_op(c):
    r0={"start":c};c0=c

    r, c = get_str(c,"and","::&")
    if 'err' not in r:
        if 0: r0['and']=r;   r0['finish']=c; return r0, c
        else : r['and']=True; r['finish']=c; return r, c

    r, c = get_str(c,"or","::|")
    if 'err' not in r:
        if 0: r0['or']=r;   r0['finish']=c; return r0, c
        else : r['or']=True; r['finish']=c; return r, c

    r, c = get_str(c,"arr","::*")
    if 'err' not in r:
        if 0: r0['arr']=r;   r0['finish']=c; return r0, c
        else : r['arr']=True; r['finish']=c; return r, c

    r['err'] = "No matches"
    return r, c0

def get_rule(c):
    r0={"start":c};c0=c

    r, c = get_id(c)
    if 'err' in r:
        return r, c
    r0['rname'] = r

    r, c = get_op(c)
    if 'err' in r:
        return r, c
    r0['op'] = r

    r, c = get_nterms(c)
    if 'err' in r:
        return r, c
    r0['terms'] = r

    r, c = get_str(c,"end",";;")
    if 'err' in r:
        return r, c
    r0['end'] = r

    r0['finish'] = c
    return r0, c

def get_program(c):
    r0={ "start":c, "program":[] }; c0=c
    while 1:
        sub=[]

        r, c = get_rule(c)
        if 'err' in r: r0['finish']=c; return r0, c0
        sub.append(r)

        c0=c; r0['program'].extend(sub)
        pass
    pass

def main():
    r,c=get_program(0)
    if repr(data[c:]): ws,c = get_ws(c)
    if data[c:]:       print "LEFTOVERS:", repr(data[c:])
    else:              print json.dumps(r, indent=4)

if __name__=='__main__': main()
