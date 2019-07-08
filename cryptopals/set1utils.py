
import math

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

###############################

def bytexor(s1, s2):
    return [c1^c2 for (c1, c2) in zip(s1, s2)]

def hexxor(h1, h2):
    return b''.join([int2base(x, alph_h, 2) for x in bytexor(hex2bytes(h1), hex2bytes(h2))])


eng_freq = {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
        'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772,
        'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095,
        'r': 5.987, 's': 6.327, 't': 2.758, 'u': 2.758, 'v': 0.987, 'w': 2.360,
        'x': 0.150, 'y': 1.974, 'z': 0.074}

eng_lfreq = {ord(k): math.log(v/100) for (k, v) in eng_freq.items()}

def likelihood(s, alph, oov):
    """Returns the log likelihood of the text s given the
    character distributions alph (log probabilities).
    oov is a function which takes a character which is used
    to handle characters not in alph
    """
    s = [alph[c] if c in alph.keys() else oov(c) for c in s]
    #print(s)
    return sum(s)

def make_punctuation_normalizer(alph):
    """ignores case, (updates alph to ignore case by adding items)
    assigns ok probability to spaces,
    somewhat low probability to common punctuation,
    and very low probability to everything else.
    *** the distribution no longer sums to 1 though

    *** need to decide on exact values for oov
    I would think we like common punctuation more than this
    but 8*m is not enough to keep from getting gibberish
    ** fine tune this on later problems?
    """
    m = min(alph.values())
    alph.update({k-32: v for (k, v) in alph.items()})
    def oov(c):
        if c == b' ':
            return 0
        if c in b',.?!()&-+=\'":;':
            return 9*m
        else:
            return 10*m
    print('updated keys to include uppercase:', len(alph.keys()))
    return oov

def guess_single_key(s, alph, oov, start=0, end=128):
    """Returns the max likelihood estimate of key xor'ed with s
    using alph as character likelihoods
    and oov as oov function.
    checks values between start and end (default 0, 128)
    """
    ms = [bytexor(s, [k]*len(s)) for k in range(start, end)]
    ls = [likelihood(m, alph, oov) for m in ms]
    besti = max(range(start, end), key=lambda x: ls[x-start])
    return besti, ms[besti], ls[besti]


