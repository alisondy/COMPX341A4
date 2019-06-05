import time
from itertools import count, islice
from math import sqrt

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


# https://stackoverflow.com/questions/4114167/checking-if-a-number-is-a-prime-number-in-python
def is_prime(n):
    if n < 2:
        return False

    for number in islice(count(2), int(sqrt(n) - 1)):
        if n % number == 0:
            return False

    return True


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def check_prime(num):
    try:
        num_p = int(num)
    except ValueError:
        return '{} is not a number'.format(num)
    if cache.get('primes') is not None:
        x = [int(i) for i in cache.get('primes').split()]
        if num_p in x:
            return '{} is a prime number'.format(num_p)
    if is_prime(num_p):
        if cache.get('primes') is not None:
            cache.append('primes', ' {}'.format(num_p))
        else:
            cache.append('primes', '{}'.format(num_p))
        return '{} is a prime number'.format(num_p)
    else:
        return '{} is not a prime number'.format(num_p)


# Credit : https://stackoverflow.com/questions/35188540/get-a-variable-from-the-url-in-a-flask-route
@app.route('/isPrime/<string:number>')
def is_prime_number(number):
    return check_prime(number)


@app.route('/primesStored')
def get_primes_stored():
    return cache.get('primes')


@app.route('/')
def hello():
    hit_count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(hit_count)
