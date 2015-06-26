#!/usr/bin/python3
# -*-coding:UTF-8 -*

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse doest not exist')
    else:
        return x % m


p = 7
q = 11

phi = (p-1)*(q-1)
print(phi)