import base64

import bcrypt


def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return base64.b64encode(hashed_password).decode('utf-8')


def verify_password(stored_hash, password):
    decoded_hash = base64.b64decode(stored_hash)
    print(decoded_hash)

    return bcrypt.checkpw(password.encode('utf-8'), decoded_hash)
