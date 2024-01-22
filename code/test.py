from utils import fnv1a_hash
import hashlib


def hash_string(s, algorithm='sha256'):
    # Create a hash object using the specified algorithm
    hash_object = hashlib.new(algorithm)

    # Update the hash object with the bytes representation of the string
    hash_object.update(s.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    return hash_object.hexdigest()

print(hash_string("HAHeweweweweweewweweA"))