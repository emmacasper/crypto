
from set1utils import hex2b64
from set1utils import hexxor
from set1utils import hex2bytes, eng_freq, single_key_breaker
from set1utils import repbxor, int2base


### part 1 ###
q1mesg = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

q1ans = b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def run_part1():
    print('running part 1...')
    print(hex2b64(q1mesg))
    print('should be')
    print(q1ans)


### part 2 ###

q2m1 = b'1c0111001f010100061a024b53535009181c'
q2m2 = b'686974207468652062756c6c277320657965'
q2ans = b'746865206b696420646f6e277420706c6179'

def run_part2():
    print('running part 2...')
    print(hexxor(q2m1, q2m2))
    print('should be')
    print(q2ans)

### part 3 ###

q3m = b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

def run_part3():
    print('running part 3...')
    k, ans, ll = single_key_breaker(hex2bytes(q3m), eng_freq)
    print('message is:', bytes(ans))
    print('key was:', k)
    print('sketchy distance measure is around:', ll)

### part 4 ###

def run_part4():
    print('running part 4...')
    opts = []
    with open('part4_message.txt', 'rb') as f:
        i = 0
        for line in f:
            if i > 0:
                break
            i += 1
        for line in f:
            opts.append(single_key_breaker(hex2bytes(line.strip()), eng_freq))
            if i > 5:
                pass
                #break
            i += 1
    besti = max(range(len(opts)), key=lambda x: opts[x][2])
    print('best message found at line', besti)
    print('message is:', bytes(opts[besti][1]))
    print('key was:', opts[besti][0])
    print('sketchy distance measure is around:', opts[besti][2])

### part 5 ###

# note that the linebreaks don't actually work, not sure what the solution wants
q5m1 = b"Burning 'em, if you ain't quick and nimble"
q5m2 = b"I go crazy when I hear a cymbal"
q5r1 = b'0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272'
q5r2 = b'a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

def run_part5():
    print('running part 5...')
    message = bytes(q5m1+b'\n'+q5m2)
    result = repbxor(message, b'ICE')
    hres = b''.join([int2base(c, b'0123456789abcdef', 2) for c in result])
    print('result is:')
    print(hres)
    print('and should be:')
    print(q5r1+q5r2)

if __name__ == '__main__':
    run_part1()
    run_part2()
    run_part3()
    run_part4()
    run_part5()
