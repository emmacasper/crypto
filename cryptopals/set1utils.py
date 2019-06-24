

def hex2bytes(x):
    """turns a hex string (string or bytes) into the equaivalent values in bytes"""
    if type(x) != type(b'h'):
        x = bytes(x)
    if len(x) % 2 == 1:
        x = b'0' + x
    alph = b'0123456789abcdef'
    return bytes([16*alph.index(x[2*i]) + alph.index(x[2*i+1]) for i in range(int(len(x)/2))])

def base2int(s, alph):
    i = 0
    print(alph)
    for c in s:
        print(c)
        i *= len(alph)
        i += alph.index(c)
    return i

def int2base(i, alph, padlen=1):
    """translates int i into some base using alph as digits
    returns bytes string; alph should be bytes or bytes list
    frontpads with zero-equivalents to make sure it is at least padlen long.
    """
    s = []
    while i > 0:
        s.insert(0, alph[i % len(alph)])
        i = int(i / len(alph))
    extra = padlen - len(s)
    s = [alph[0]]*extra + s
    return bytes(s)

alph64 = list(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
alph_h = list(b'0123456789abcdef')
alph256 = list(range(256))

def chunk64(c):
    return int2base(base2int(c, alph256), alph64, 4)

def chunk64last(c):
    if len(c) == 3:
        return chunk64(c)
    if len(c) == 2:
        return bytes(int2base(base2int(c, alph256)*4, alph64, 3) + b'=')
    else:
        return bytes(int2base(base2int(c, alph256)*16, alph64, 2) + b'==')

def hex2b64(x):
    x = hex2bytes(x)
    result = [chunk64(x[i*3:i*3+3]) for i in range(len(x)//3)]
    if len(x) % 3 != 0:
        print('extra chunk')
        print(b''.join(result))
        result.append(chunk64last(x[-(len(x)%3):]))
    return b''.join(result)
