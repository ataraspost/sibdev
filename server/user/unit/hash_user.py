
"""Всегда инфарианта для двух целых чисел"""
def get_hash_user(a, b):
    if a > b:
        a,b = b,a
    return ((a+b)*(a+b+1))/2 + a
