def str_xor(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1, s2)])


def msgencode(message, key):
    return str_xor(message, key)


def msgdecode(encoded, key):
    return str_xor(encoded, key)
