import hashlib

from jose import jwt


def has_file(file_path):
    file = file_path
    BLOCK_SIZE = 65536  # The size of each read from the file
    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(BLOCK_SIZE)  # Read the next block from the file
        print(file_hash.hexdigest())  # Get the hexadecimal digest of the hash
    return file_hash.hexdigest()


def generate_token(user):
    secret = 'amf1234'
    algorithm = 'HS256'
    token = jwt.encode(user, secret, algorithm)
    return token


def decode_token(token):
    secret = 'amf1234'
    algorithm = 'HS256'
    user = jwt.decode(token, secret, algorithm)
    return user