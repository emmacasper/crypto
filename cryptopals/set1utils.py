
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
    for c in s:
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
        result.append(chunk64last(x[-(len(x)%3):]))
    return b''.join(result)

###############################

def bytexor(s1, s2):
    return [c1^c2 for (c1, c2) in zip(s1, s2)]

def hexxor(h1, h2):
    return b''.join([int2base(x, alph_h, 2) for x in bytexor(hex2bytes(h1), hex2bytes(h2))])


eng_freq = {ord(k): v/100 for (k, v) in {'a': 8.167, 'b': 1.492,
        'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015,
        'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 
        'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095,
        'r': 5.987, 's': 6.327, 't': 2.758, 'u': 2.758, 'v': 0.987,
        'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074}.items()}

def bhattacharyya_coefficient(d1, d2):
    """Computes the bhattacharyya coefficient of two distributions
    Distributions should have the same keyset to work properly
    (if d2 has extra keys it will not break but will be incorrect).

    Bhattacharyya coefficient is sum over x of prob(x) in each distribution

    *** do not call this if no keys overlap. bad things will happen.
    """
    coeff = sum([math.sqrt(d1[k]*d2.get(k, 0)) for k in d1.keys()])
    return coeff

def frequency_fit(alph, sample):
    """A somewhat sketchy measure of how likely the sample came from
    the alphabet distribution.
    (likely in the colloquial sense, not the probabilistic one)
    Some penalty for characters not in alph, excluding spaces
    Ignores case
    """
    # number of non-space characters
    l = len(sample) - len(bytes(sample).split()) + 1
    sample = [x for x in bytes(sample).lower()]
    counter = {}
    for c in sample:
        if c in alph.keys():
            counter[c] = counter.get(c, 0) + 1
    # make it a distribution, sort of
    scount = {k: v/l for (k, v) in counter.items()}
    if len(scount.keys()) == 0:
        # if we actually call bhattacharyya distance it will cry
        # pick a big number because we do not like this.
        return 0
    return bhattacharyya_coefficient(alph, scount)
    

def single_key_breaker(s, alph, start=0, end=128):
    """Returns the best estimate of key xor'ed with s
    using alph as character likelihoods
    checks values between start and end (default 0, 128)
    """
    ms = [bytexor(s, [k]*len(s)) for k in range(start, end)]
    ls = [frequency_fit(alph, m) for m in ms]
    besti = max(range(start, end), key=lambda x: ls[x-start])
    return besti, ms[besti], ls[besti]


def repbxor(s, k):
    l = int(len(s)/ len(k)) + 1
    return bytexor(s, (k*l)[:len(s)])

def rephxor(s, k):
    return repbxor(hex2bytes(s), hex2bytes(k))

