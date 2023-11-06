import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def verify_password_hash(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)