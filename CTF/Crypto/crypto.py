import random
import math
from collections import defaultdict
def modexp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result
def generate_parameters():
    p = 467   
    g = 2    
    return p, g
def generate_keys(p, g):
    priv = random.randint(2, p - 2)
    pub = modexp(g, priv, p)
    return priv, pub
def sharedsecret(other_pub, own_priv, p):
    return modexp(other_pub, own_priv, p)
def bruteforce(g, p, public_key):
    for priv in range(1, p):
        if modexp(g, priv, p) == public_key:
            return priv
    return None
def bsgs(g, h, p):
    N = int(math.isqrt(p - 1)) + 1
    baby_steps = {}
    for j in range(N):
        baby_steps[modexp(g, j, p)] = j
    g_inv_N = modexp(g, -N % (p - 1), p)
    current = h
    for i in range(N):
        if current in baby_steps:
            return i * N + baby_steps[current]
        current = (current * g_inv_N) % p
    return None
def sim():
    print("Diffie-Hellman")
    p, g = generate_parameters()
    print(f"Public Parameters:\np = {p}\ng = {g}")
    a_priv, a_pub = generate_keys(p, g)
    b_priv, b_pub = generate_keys(p, g)
    print(f"\nUser 1 Public Key: {a_pub}")
    print(f"User 2 Public Key: {b_pub}")
    a_secret = sharedsecret(b_pub, a_priv, p)
    b_secret = sharedsecret(a_pub, b_priv, p)
    print(f"\nShared Secret (User1): {a_secret}")
    print(f"Shared Secret (User2):   {b_secret}")
    assert a_secret == b_secret
    print("\n\nBrute Force")
    recovered_priv = bruteforce(g, p, a_pub)
    print(f"Recovered User1 Private Key: {recovered_priv}")
    recovered_secret = sharedsecret(b_pub, recovered_priv, p)
    print(f"Recovered Shared Secret: {recovered_secret}")
    assert recovered_secret == a_secret
    print("\n\nBSGS")
    p_large = 104729 
    g_large = 2
    priv_large = random.randint(2, p_large - 2)
    pub_large = modexp(g_large, priv_large, p_large)
    print(f"{g_large}^x ≡ {pub_large} mod {p_large}")
    recovered = bsgs(g_large, pub_large, p_large)
    print(f"x = {recovered}")
    assert modexp(g_large, recovered, p_large) == pub_large

if __name__ == "__main__":
    sim()
