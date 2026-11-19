import random
import sympy
from math import gcd

def generate_prime(bits):
	num = random.getrandbits(bits)
	while not sympy.isprime(num):
		num+=1
	return num

def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)

    while p == q:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = generate_prime(bits)

    while e < phi and gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


def encrypt(message, public_key):
    e, n = public_key

    encrypted = []

    for char in message:
        m = ord(char)

        encrypted.append(pow(m, e, n))

    return encrypted

def decrypt(encrypted, private_key):
    d, n = private_key

    message = ''

    for char in encrypted:
        m = pow(char, d, n)

        message += chr(m)

    return message

def save_keys(public_key, private_key):
    with open('public_key.txt', 'w') as public:
        public.write(f'{public_key[0]}\n{public_key[1]}')

    with open('private_key.txt', 'w') as private:
        private.write(f'{private_key[0]}\n{private_key[1]}')
        

public_key, private_key = generate_keys(512)

print(f'Открытый ключ: {public_key}')
print(f'Закрытый ключ: {private_key}')

save_keys(public_key, private_key)

message = input('Введите сообщение: ')
enc = encrypt(message, public_key)
dec = decrypt(enc, private_key)

print(f'Зашифрованное сообщение: {enc}')
print(f'Расшифрованное сообщение: {dec}')