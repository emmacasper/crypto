
from set1utils import hex2b64

### part 1 ###
part1mesg = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

part1ans = b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def run_part1():
    print(hex2b64(part1mesg))
    print('should be')
    print(part1ans)



